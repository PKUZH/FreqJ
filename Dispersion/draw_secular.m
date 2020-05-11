load layer_deep.mat
layer_z = layer(:, 1);%m
layer_rou = layer(:, 2);%kg/m^3
layer_alpha = layer(:, 3);%m/s
layer_beta = layer(:, 4);%m/s

layer_mu = layer_beta.^2.*layer_rou;

layer_num = size(layer, 1);

f = 1; % Hz
[cmin, cmax, dc] = deal(2800, 4800, 1); % m/s
c = cmin-dc/2:dc:cmax+dc/2; % to avoid singular at media's beta
dets = ones(layer_num, size(c, 2));

for j = 1:size(c, 2)
    dets(:,j) = cal_det(f,c(j), layer_z, layer_alpha, layer_beta, layer_mu);
end

for j = 1:layer_num
    figure
    dets(j,:) = dets(j,:) / max(dets(j,:)); % normalize
    plot(c,dets(j,:), 'LineWidth', 2);
    xlabel('phase velocity (km/s)')
    ylabel('|secular func(v,f)|')
end