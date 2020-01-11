function dets = cal_det(f,c,z_l,alpha,beta,mu)
    w = 2*pi*f;
    l_num = size(alpha,1);
    k = w/c;
    gamma = sqrt(k^2-(w./alpha).^2);
    vu = sqrt(k^2-(w./beta).^2);
    x = k^2+vu.^2;
    %define E Matrix
    E11 = zeros(l_num,2,2);
    E12 = zeros(l_num,2,2);
    E21 = zeros(l_num,2,2);
    E22 = zeros(l_num,2,2);
    for j = 1:l_num
        E11(j,:,:) = [alpha(j)*k beta(j)*vu(j);alpha(j)*gamma(j) beta(j)*k]/w;
        E12(j,:,:) = [alpha(j)*k beta(j)*vu(j);-alpha(j)*gamma(j) -beta(j)*k]/w;
        E21(j,:,:) = [-2*alpha(j)*mu(j)*k*gamma(j) -beta(j)*mu(j)*x(j);-alpha(j)*mu(j)*x(j) -2*beta(j)*mu(j)*k*vu(j)]/w;
        E22(j,:,:) = [2*alpha(j)*mu(j)*k*gamma(j) beta(j)*mu(j)*x(j);-alpha(j)*mu(j)*x(j) -2*beta(j)*mu(j)*k*vu(j)]/w;
    end
    %define R/T 
    T_d = zeros(l_num-1,2,2);
    R_du = zeros(l_num-1,2,2);
    T_u = zeros(l_num-2,2,2);
    R_ud = zeros(l_num-1,2,2);
    [~,Lambda_u] = cal_Lambda(0,z_l,vu,gamma,l_num);
    Lambda_u_0 = reshape(Lambda_u(1,:,:),2,2);
    E21_0 = reshape(E21(1,:,:),2,2);
    E22_0 = reshape(E22(1,:,:),2,2);
    R_ud(1,:,:) = -pinv(E21_0)*E22_0*Lambda_u_0;
    for j = 1:l_num-2
        E11_1 = reshape(E11(j+1,:,:),2,2);
        E12_1 = reshape(E12(j+1,:,:),2,2);
        E21_1 = reshape(E21(j+1,:,:),2,2);
        E22_1 = reshape(E22(j+1,:,:),2,2);
        E11_0 = reshape(E11(j,:,:),2,2);
        E12_0 = reshape(E12(j,:,:),2,2);
        E21_0 = reshape(E21(j,:,:),2,2);
        E22_0 = reshape(E22(j,:,:),2,2);
        [Lambda_d,Lambda_u] = cal_Lambda(z_l(j+1),z_l,vu,gamma,l_num);
        Lambda_d_0 = reshape(Lambda_d(j,:,:),2,2);
        Lambda_u_1 = reshape(Lambda_u(j+1,:,:),2,2);
        M = pinv([E11_1 -E12_0;E21_1 -E22_0])*[E11_0 -E12_1;E21_0 -E22_1]*[Lambda_d_0 zeros(2,2);zeros(2,2) Lambda_u_1];
        T_d(j,:,:) = M(1:2,1:2);
        R_du(j,:,:) = M(3:4,1:2);
        R_ud(j+1,:,:) = M(1:2,3:4);
        T_u(j,:,:) = M(3:4,3:4);
    end
    for j = l_num-1
        E11_1 = reshape(E11(j+1,:,:),2,2);
        E21_1 = reshape(E21(j+1,:,:),2,2);
        E11_0 = reshape(E11(j,:,:),2,2);
        E12_0 = reshape(E12(j,:,:),2,2);
        E21_0 = reshape(E21(j,:,:),2,2);
        E22_0 = reshape(E22(j,:,:),2,2);
        [Lambda_d,~] = cal_Lambda(z_l(j+1),z_l,vu,gamma,l_num);
        Lambda_d_0 = reshape(Lambda_d(j,:,:),2,2);
        M = pinv([E11_1 -E12_0;E21_1 -E22_0])*[E11_0*Lambda_d_0;E21_0*Lambda_d_0];
        T_d(j,:,:) = M(1:2,1:2);
        R_du(j,:,:) = M(3:4,1:2);
    end
    %define generalized R/T
    T_d_new = zeros(l_num-1,2,2);
    R_du_new = zeros(l_num-1,2,2);
    T_u_new = zeros(l_num-2,2,2);
    R_ud_new = zeros(l_num-1,2,2);
    R_ud_new(1,:,:) = reshape(R_ud(1,:,:),2,2);
    for j = 2:l_num-1
        R_ud_new_0 = reshape(R_ud_new(j-1,:,:),2,2);
        R_du_0 = reshape(R_du(j-1,:,:),2,2);
        T_u_0 = reshape(T_u(j-1,:,:),2,2);
        T_u_new_0 = pinv(eye(2)-R_du_0*R_ud_new_0)*T_u_0;
        R_ud_0 = reshape(R_ud(j,:,:),2,2);
        T_d_0 = reshape(T_d(j-1,:,:),2,2);
        R_ud_new_0 = R_ud_0+T_d_0*R_ud_new_0*T_u_new_0;
        T_u_new(j-1,:,:) = T_u_new_0;
        R_ud_new(j,:,:) = R_ud_new_0;
    end
    for j = l_num-1
        T_d_new(j,:,:) = reshape(T_d(j,:,:),2,2); 
        R_du_new(j,:,:) = reshape(R_du(j,:,:),2,2);
    end
    for j = l_num-2:-1:1
        T_d_0 = reshape(T_d(j,:,:),2,2);
        T_u_0 = reshape(T_u(j,:,:),2,2);
        R_ud_0 = reshape(R_ud(j+1,:,:),2,2);
        R_du_new_0 = reshape(R_du_new(j+1,:,:),2,2);
        T_d_new_0 = pinv(eye(2)-R_ud_0*R_du_new_0)*T_d_0;
        R_du_0 = reshape(R_du(j,:,:),2,2);
        R_du_new_0 = R_du_0+T_u_0*R_du_new_0*T_d_new_0;
        T_d_new(j,:,:) = T_d_new_0; 
        R_du_new(j,:,:) = R_du_new_0;
    end
    dets = zeros(l_num,1);
    for j = 1:l_num-1
        R_ud_new_0 = reshape(R_ud_new(j,:,:),2,2);
        R_du_new_0 = reshape(R_du_new(j,:,:),2,2);
        dets(j) = det(eye(2)-R_ud_new_0*R_du_new_0);
    end
    E21_0 = reshape(E21(1,:,:),2,2);
    E22_0 = reshape(E22(1,:,:),2,2);
    R_du_new_0 = reshape(R_du_new(1,:,:),2,2);
    [~,Lambda_u] = cal_Lambda(0,z_l,vu,gamma,l_num);
    Lambda_u_0 = reshape(Lambda_u(1,:,:),2,2);
    dets(l_num) = det(E21_0-E22_0*Lambda_u_0*R_du_new_0);
end

function [Lambda_d,Lambda_u] = cal_Lambda(z,z_l,vu,gamma,l_num)
    Lambda_d = zeros(l_num,2,2);
    Lambda_u = zeros(l_num-1,2,2);
    for j = 1:l_num
        Lambda_d(j,:,:) = [exp(-gamma(j)*(z-z_l(j))) 0;0 exp(-vu(j)*(z-z_l(j)))];
    end
    for j = 1:l_num-1
        Lambda_u(j,:,:) = [exp(-gamma(j)*(z_l(j+1)-z)) 0;0 exp(-vu(j)*(z_l(j+1)-z))];
    end      
end