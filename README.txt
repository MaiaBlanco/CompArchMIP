Project Members:
Mark Blanco and Aayushya Agarwal

This is a copy of our code, located here: https://github.com/MarkBlanco/CompArchMIP

This code needs to be placed in the /workspace directory of the docker container located here:
https://hub.docker.com/r/xyzsam/gem5-aladdin/

Alternatively you can pull this docker container and update the copy of this repository located at /workspace:
https://hub.docker.com/r/markblanco/mip_container_img/
Be sure to pull the image with tag :second if using the link immediately above. You may also need to recompile gem5-aladdin in that container.

Directories:
mat_inv: contains aladdin-only Gauss-Jordan Elimination Algorithm
mat_inv_with_cpu: contains source and parameter sweeping scripts for gem5-aladdin GJE matrix inverse accelerator.
mat_soln_with_cpu: contains source and parameter sweeping scripts for gem5-aladdin GJE system solving accelerator.
sw_src: contains early matrix inverse algorithm tests including OpenMP GJE implementation and code to read matrix markex formatted files.
results: contains spreadsheets of results of several design runs and several scripts to plot and analyze design points.