function zerov = find_zero(w,c,layer_z,layer_alpha,layer_beta,layer_mu,err)
    v = c;
    det_result = c;
    for j = 1:size(v,2)
        k = cal_det(w,v(j),layer_z,layer_alpha,layer_beta,layer_mu);
        det_result(j) = abs(k(1))*abs(k(2))*abs(k(3))*abs(k(4));
    end
    det_max = max(det_result);
    det_mean = mean(det_result);
    while det_max>5*det_mean
        num = find(det_result == det_max);
        v(num) = [];
        det_result(num) = [];
        det_max = max(det_result);
        det_mean = mean(det_result);
    end
    det_result= det_result/det_max;
    len = size(v,2);
    zerov = [];
    for i = 2:len-1
        if det_result(i)<min([det_result(i-1),det_result(i+1),err])&&(ismember(v(i),layer_beta)~=1)
            zerov = [zerov,v(i)];
        end
    end
    if size(zerov,2)>0
        zerov(1) =[];
    end
end