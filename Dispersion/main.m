load layer.mat
layer_z = layer(:,1);%m
layer_rou = layer(:,2);%kg/m^3
layer_alpha = layer(:,3);%m/s
layer_beta = layer(:,4);%m/s

layer_mu = layer_beta.^2.*layer_rou;

err = 0.004;
f = 0.001:0.001:25;
c = 150:600;
fsa = [];
vsa = [];
for j = 1:size(f,2)
    zerov = find_zero(f(j),c,layer_z,layer_alpha,layer_beta,layer_mu,err);
    fs = ones(1,size(zerov,2))*f(j);
    fsa = [fsa,fs];
    vsa = [vsa,zerov];
disp(j)
end
save result1.mat fsa vsa
