%
% Copyright (c) 2015, Yarpiz (www.yarpiz.com)
% All rights reserved. Please read the "license.txt" for license terms.
%
% Project Code: YPAP108
% Project Title: Solving Vehicle Routing Problem using Simulated Annealing
% Publisher: Yarpiz (www.yarpiz.com)
% 
% Developer: S. Mostapha Kalami Heris (Member of Yarpiz Team)
% 
% Contact Info: sm.kalami@gmail.com, info@yarpiz.com
%

function PlotSolution(sol,model)

    J=model.J;

    xmin=model.xmin;
    xmax=model.xmax;
    ymin=model.ymin;
    ymax=model.ymax;
    
    x=model.x;
    y=model.y;
    x0=model.x0;
    y0=model.y0;
    
    L=sol.L;
    
    Colors=hsv(J);
    
    for j=1:J
        
        if isempty(L{j})
            continue;
        end
        
        X=[x0 x(L{j}) x0];
        Y=[y0 y(L{j}) y0];
        
        Color=0.8*Colors(j,:);
        
        plot(X,Y,'-o',...
            'Color',Color,...
            'LineWidth',2,...
            'MarkerSize',10,...
            'MarkerFaceColor','white');
        hold on;
        
    end

    plot(x0,y0,'ks',...
        'LineWidth',2,...
        'MarkerSize',18,...
        'MarkerFaceColor','yellow');
    
    hold off;
    grid on;
    axis equal;
    
    xlim([xmin xmax]);
    ylim([ymin ymax]);
    
end












