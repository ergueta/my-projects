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

clc;
clear;
close all;

%% Problem Definition

model=SelectModel();        % Select Model of the Problem

model.eta=0.1;

CostFunction=@(q) MyCost(q,model);       % Cost Function

%% SA Parameters

MaxIt=1200;     % Maximum Number of Iterations

MaxIt2=80;      % Maximum Number of Inner Iterations

T0=100;         % Initial Temperature

alpha=0.98;     % Temperature Damping Rate


%% Initialization

% Create Initial Solution
x.Position=CreateRandomSolution(model);
[x.Cost, x.Sol]=CostFunction(x.Position);

% Update Best Solution Ever Found
BestSol=x;

% Array to Hold Best Cost Values
BestCost=zeros(MaxIt,1);

% Set Initial Temperature
T=T0;


%% SA Main Loop

for it=1:MaxIt
    for it2=1:MaxIt2
        
        % Create Neighbor
        xnew.Position=CreateNeighbor(x.Position);
        [xnew.Cost, xnew.Sol]=CostFunction(xnew.Position);
        
        if xnew.Cost<=x.Cost
            % xnew is better, so it is accepted
            x=xnew;
            
        else
            % xnew is not better, so it is accepted conditionally
            delta=xnew.Cost-x.Cost;
            p=exp(-delta/T);
            
            if rand<=p
                x=xnew;
            end
            
        end
        
        % Update Best Solution
        if x.Cost<=BestSol.Cost
            BestSol=x;
        end
        
    end
    
    % Store Best Cost
    BestCost(it)=BestSol.Cost;

    
    % Display Iteration Information
    if BestSol.Sol.IsFeasible
        FLAG=' *';
    else
        FLAG='';
    end
    disp(['Iteration ' num2str(it) ': Best Cost = ' num2str(BestCost(it)) FLAG]);
    
    % Reduce Temperature
    T=alpha*T;
    
    % Plot Solution
    figure(1);
    PlotSolution(BestSol.Sol,model);
    pause(0.01);
    
end

%% Results

figure;
plot(BestCost,'LineWidth',2);
xlabel('Iteration');
ylabel('Best Cost');
grid on;

