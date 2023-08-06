/*
 *   Project: 2D Diffraction images peak finding and integrating.
 *            OpenCL Kernels  
 *
 *
 *   Copyright (C) 2012-2019 European Synchrotron Radiation Facility
 *                           Grenoble, France
 *
 *   Principal authors: J. Kieffer (kieffer@esrf.fr)
 *   Last revision: 04/12/2019
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

/* Constant to be provided at build time:
 *   WORKGROUP_SIZE: number of threads in a workgroup, 1024 is a good bet.
 *   NIMAGE: size of the image
 */

#include "for_eclipse.h"


/* Pixel-wise kernel that calculated the I-bg and counting pixels of interest
 * 
 * For every pixel in the preproc array, the value for the background level 
 * and the std are interpolated.
 * Pixel with (Icor-Bg)>   min(cutoff*std, noise) are marked as peak-pixel, 
 * counted and their index registered in highidx
 * 
 * The kernel uses local memory for keeping track of peak count and positions 
 */
kernel void find_peaks(       global  float4 *preproc4, //both input and output
                        const global  float  *radius2d,
                        const global  float  *radius1d,
                        const global  float  *average1d,
                        const global  float  *std1d,
                        const         float   radius_min,
                        const         float   radius_max,
                        const         float   cutoff,
                        const         float   noise,
                              global  int    *counter,
                              global  int    *highidx){
    int tid = get_local_id(0);
    int gid = get_global_id(0);
    int wg = get_local_size(0);
    // all thread in this WG share this local counter, upgraded at the end
    volatile local int local_counter[2];
    volatile local int local_highidx[WORKGROUP_SIZE];
    // Ensure wg <= WORKGROUP_SIZE
    local_highidx[tid] = 0;
    for (int i=0; i<2; i+=wg){
        if (i+tid < 2){
            local_counter[i+tid] = 0;
        }
    }
    barrier(CLK_LOCAL_MEM_FENCE);    
    
    if (gid<NIMAGE) {
        float radius = radius2d[gid];
        float4 value = (float4)(0.0f, 0.0f, 0.0f, 0.0f);
        if (isfinite(radius) && (radius>=radius_min) && (radius<radius_max)) {
            value = preproc4[gid];
            if (value.s2>0.0) {
                value.s1 = value.s0 / value.s2; 
            } // normalization not null -> calculate corrected value
            else {
                value.s0 = 0.0f;
                value.s1 = 0.0f;
            } // empty pixel
            float pos = (radius - radius1d[0]) /  (radius1d[1] - radius1d[0]);
            int index = convert_int_rtz(pos);
            float delta = pos - index;
            value.s2 = average1d[index]*(1.0f-delta) + average1d[index+1]*(delta); // bilinear interpolation: averge
            value.s3 = std1d[index]*(1.0f-delta) + std1d[index+1]*(delta); // bilinear interpolation: std
            if ((value.s1 - value.s2) > max(noise, cutoff*value.s3)){
                local_highidx[atomic_inc(local_counter)] = gid;
            }//pixel is considered of high intensity: registering it. 
        } //check radius range
        preproc4[gid] = value;
    } //pixel in image
    
    //Update global memory counter
    barrier(CLK_LOCAL_MEM_FENCE);
    if (local_counter[0]){
        if (tid == 0) 
            local_counter[1] = atomic_add(counter, local_counter[0]);
        barrier(CLK_LOCAL_MEM_FENCE);
        if (tid<local_counter[0])
            highidx[tid +local_counter[1]] = local_highidx[tid];
    } // end update global memory

} //end kernel find_peaks

// function returning the diffraction signal intensity i.e. (Icorrected - Ibackground)
static float _calc_intensity(float4 value){
	return value.s1 - value.s2;
}

// A simple kernel to copy the intensities of the peak

kernel void copy_peak(global int *peak_position,
                      global int *counter,
                      global float4 *preprocessed,
                      global float *peak_intensity){
    int cnt, tid;
    tid = get_global_id(0);    
    cnt = counter[0];
    if (tid<cnt){
        peak_intensity[tid] = preprocessed[peak_position[tid]].s0;
    }
}

kernel void copy_peak_uint8(global int *peak_position,
                      global int *counter,
                      global float4 *preprocessed,
                      global unsigned char *peak_intensity){
    int cnt, tid;
    tid = get_global_id(0);    
    cnt = counter[0];
    if (tid<cnt){
        peak_intensity[tid] = (unsigned char)(preprocessed[peak_position[tid]].s0+0.5f);
    }
}

kernel void copy_peak_int8(global int *peak_position,
                      global int *counter,
                      global float4 *preprocessed,
                      global char *peak_intensity){
    int cnt, tid;
    tid = get_global_id(0);    
    cnt = counter[0];
    if (tid<cnt){
        peak_intensity[tid] = (char)(preprocessed[peak_position[tid]].s0+0.5f);
    }
}

kernel void copy_peak_uint16(global int *peak_position,
                      global int *counter,
                      global float4 *preprocessed,
                      global unsigned short *peak_intensity){
    int cnt, tid;
    tid = get_global_id(0);    
    cnt = counter[0];
    if (tid<cnt){
        peak_intensity[tid] = (unsigned short)(preprocessed[peak_position[tid]].s0+0.5f);
    }
}

kernel void copy_peak_int16(global int *peak_position,
                      global int *counter,
                      global float4 *preprocessed,
                      global short *peak_intensity){
    int cnt, tid;
    tid = get_global_id(0);    
    cnt = counter[0];
    if (tid<cnt){
        peak_intensity[tid] = (short)(preprocessed[peak_position[tid]].s0+0.5f);
    }
}

kernel void copy_peak_uint32(global int *peak_position,
                      global int *counter,
                      global float4 *preprocessed,
                      global unsigned int *peak_intensity){
    int cnt, tid;
    tid = get_global_id(0);    
    cnt = counter[0];
    if (tid<cnt){
        peak_intensity[tid] = (unsigned int)(preprocessed[peak_position[tid]].s0+0.5f);
    }
}

kernel void copy_peak_int32(global int *peak_position,
                      global int *counter,
                      global float4 *preprocessed,
                      global int *peak_intensity){
    int cnt, tid;
    tid = get_global_id(0);    
    cnt = counter[0];
    if (tid<cnt){
        peak_intensity[tid] = (int)(preprocessed[peak_position[tid]].s0+0.5f);
    }
}


/* this kernel takes the list of high-pixels, searches for the local maximum.
 * 
 * the index of this maximum is saved into the pixel position.
 * the counter of the local maximum is incremented.
 * 
 * 
 * This kernel has to be launched with one thread per hot pixel.
 */


kernel void seach_maximum(       global  float4 *preproc4, //both input and output
		                   const global  int    *highidx,
						   const         int     nbhigh,
						   const         int     width,
						   const         int     height,
						   
                                 global  int    *peak_size){
	//Nota preproc4 contains Iraw, Icor, Ibg, sigma
	int gid = get_global_id(0);
	if (gid<nbhigh) {
		int here = highidx[gid];
		if (here<NIMAGE){
			int x, y, where, there;
			float4 value4 = preproc4[here];
			float value = _calc_intensity(value4);
			where = 0; // where is left at zero if we are on a local maximum
			//TODO: finish
		}
	}
	
}

/* this kernel takes an images 
kernel void peak_dilation(){
	TODO
}
*/