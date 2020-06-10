load('model/layer_shallow.mat')
layer_z = layer(:,1);%m
layer_rou = layer(:,2);%kg/m^ 3
layer_alpha = layer(:,3);%m/s
layer_beta = layer(:,4);%m/s

layer_mu = layer_beta.^2.*layer_rou;

err = 0.0001;
f = 0.025: 0.025: 25 ;
c = [170,600,0.1];
dc = c(3);

fsa = [];
vsa = [];
for j = 1:size(f,2)
    zerov = find_zero(f(j),c,layer_z,layer_alpha,layer_beta,layer_mu,err);
    
%     [zerov, det_maxs] = find_zero(f(j),c,layer_z,layer_alpha,layer_beta,layer_mu,err); 
%     times = 0;
%     err_new = err;
%     while times<0
%         err_new = err_new;
%         zerov_new = [];
%         for it = 1:size(zerov, 2)
%             c_new = [zerov(it)-dc,zerov(it)+dc,dc/10];
%             c_zero_new = find_zero(f(j),c_new,layer_z,layer_alpha,layer_beta,layer_mu,err_new, 1, det_maxs);
%             zerov_new = [zerov_new,c_zero_new];
%         end
%         dc = dc/10;
%         times = times+1;
%         zerov = zerov_new;
%     end

    fs = ones(1,size(zerov,2))*f(j);
    fsa = [fsa,fs];
    vsa = [vsa,zerov];
    disp(j)
end
plot(fsa,vsa,'*')
save result_shallow.mat fsa vsa
