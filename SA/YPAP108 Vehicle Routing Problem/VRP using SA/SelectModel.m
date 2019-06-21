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

function model=SelectModel()

    Filter={'*.mat','MAT Files (*.mat)'
            '*.*','All Files (*.*)'};

    [FileName, FilePath]=uigetfile(Filter,'Select Model ...');
    
    if FileName==0
        model=[];
        return;
    end
    
    FullFileName=[FilePath FileName];
    
    data=load(FullFileName);
    
    model=data.model;

end