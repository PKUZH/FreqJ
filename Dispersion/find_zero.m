function zerov = find_zero(f,c,layer_z,layer_alpha,layer_beta,layer_mu,err)
    zerov = [];
    [cmin,cmax,dc] = deal(c(1),c(2),c(3));
    c_ls = cmin-dc/2:dc:cmax+dc/2;
    det_num = size(layer_z,1);
    det_len = size(c_ls,2);
    det_ls = zeros(det_num,det_len);
    
%     det_maxs = zeros(det_len,1);
    for j = 1:size(c_ls,2)
        det_ls(:,j) = cal_det(f,c_ls(j),layer_z,layer_alpha,layer_beta,layer_mu);
    end
    for k = 1:size(layer_z,1)
        det_maxs(k,1) = max(det_ls(k,:));
        det_ls(k,:) = det_ls(k,:) / max(det_ls(k,:));
    end
    for j = 1:size(c_ls,2)
        if is_zero(j, det_ls, det_num, det_len, err) && (ismember(c_ls(j),layer_beta+dc/2)~=1)...
           && (ismember(c_ls(j),layer_beta-dc/2)~=1) && ((size(zerov,2)==0) || (min(abs(zerov-c_ls(j)))>10*dc))
            zerov = [zerov,c_ls(j)];
        end
    end
    
%     else
%         for k = 1:size(layer_z,1)
%             det_ls(k,:) = det_ls(k,:) / det_max(k,1);
%         end
%         for j = 1:size(c_ls,2)
%             if is_zero(j, det_ls, det_num, det_len, err) && ...
%                     ((size(zerov,2)==0) || (min(abs(zerov-c_ls(j)))>10*dc))
%                 zerov = [zerov,c_ls(j)];
%             end
%         end 
%     end

end


function is = is_zero(j, det_ls, det_num, det_len, delta)
    if j~=1 && j~=det_len
        for k = 1:det_num
            det_left = det_ls(k,j-1);
            det_right = det_ls(k,j+1);
            if det_ls(k,j)< min([delta, det_left, det_right])
                is = 1;
                return
            end
        end
    end
    is = 0;
end
                
        
  