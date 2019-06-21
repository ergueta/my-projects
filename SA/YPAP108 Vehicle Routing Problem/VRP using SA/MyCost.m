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

function [z, sol]=MyCost(q,model)

    sol=ParseSolution(q,model);
    
    eta=model.eta;
    
    z1=eta*sol.TotalD+(1-eta)*sol.MaxD;
    
    beta=5;
    
    z=z1*(1+beta*sol.MeanCV);

end