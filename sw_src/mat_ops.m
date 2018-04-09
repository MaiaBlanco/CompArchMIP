% Load known sparse matrix, compute inverse, and export the resulting dense
% inverse.
B = mmload('1138_bus.mtx');
B_inv = B^-1;
B_inv_d = full(B_inv);
mmwrite('1138_bus_known_inverse.mmx', B_inv_d);

% Determine the sparsity of the original and inverse matrices:
sz_B = size(B);
num_elems = sz_B(1) * sz_B(2);
sp_B = 1-nnz(B) / num_elems;
sp_inv = 1-nnz(B_inv) / num_elems;
fprintf('Matrix B is %f percent sparse.\n', sp_B);
fprintf('Matrix B_inv is %f percent sparse.\n', sp_inv);

% Create b and x vectors to create a system that can be solved, such that 
% Bx = b.
b = sprand(sz_B(1), 1, 0.5);
x = B_inv * b;
B_check = B*x;

% NOTE: if x is solved by b\B, result differs from solving by B_inv*b
% This must be due to numeric instability.