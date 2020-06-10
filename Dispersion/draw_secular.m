load layer_shallow.mat
layer_z = layer(:, 1);%m
layer_rou = layer(:, 2);%kg/m^3
layer_alpha = layer(:, 3);%m/s
layer_beta = layer(:, 4);%m/s

layer_mu = layer_beta.^2.*layer_rou;

layer_num = size(layer, 1);

f = 15; % Hz
[cmin, cmax, dc] = deal(180, 600, 0.1); % m/s
c = cmin-dc/2:dc:cmax+dc/2; % to avoid singular at media's beta
dets = ones(layer_num, size(c, 2));

for j = 1:size(c, 2)
    dets(:,j) = cal_det(f,c(j), layer_z, layer_alpha, layer_beta, layer_mu);
end

for j = 1:layer_num
    figure
    dets(j,:) = dets(j,:) / max(dets(j,:)); % normalize
    plot(c,dets(j,:), 'LineWidth', 2);
    hold on
    plot(c,zeros(1,size(c,2)),'r','LineWidth', 1);
    xlabel('phase velocity (m/s)','FontSize',20)
    ylabel('|secular func(v,f)|','FontSize',20)
    xlim([170 610])
    ylim([-0.1 1.1])
    title(['Secular function in layer ',num2str(rem(j,4))],'FontSize',30);
    set(gca,'FontSize',20)
end