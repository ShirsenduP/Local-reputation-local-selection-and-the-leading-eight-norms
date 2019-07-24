function Adj=lattice_structure(N)
% Create a lattice structure of size N, symilar to the one of figure S12 of
% Righi S., Takacs K. (2018) "Social Closure and the Evolution of
% Cooperation via Indirect Reciprocity", Scientific Reports
% a regular lattice with a homogenous degree is created and the same number of closed triads for each agent. 
% We create cliques of four nodes, and exactly one tie to a non-clique member in a regular way (Fig. S12).

baseclique=ones(4,4);
for i=1:4
   baseclique(i,i)=0;
end

Adj=zeros(N,N);

startpos=1;
endpos=4;
whichone=3;
for i=1:N/4
    Adj(startpos:endpos,startpos:endpos)=baseclique; %set the basecliques around the diagonal
    if i>1
        if whichone(i-1)==3; whichone(i)=1; else whichone(i)=3; end % keep track of the connection point
    end
   if whichone(i)==3 && endpos+whichone(i)<=N
        Adj(endpos,endpos+whichone(i))=1;
        Adj(endpos+whichone(i),endpos)=1;
   end
    if whichone(i)==1 && endpos+whichone(i)<=N
        Adj(endpos+whichone(i),startpos+whichone(i))=1;
        Adj(startpos+whichone(i),endpos+whichone(i))=1;
    end
    if i==(N/4)
        if whichone(i)==3
            Adj(end,whichone(i))=1;
            Adj(whichone(i),end)=1;
        end
        if whichone(i)==1
            Adj(startpos+whichone(i),1)=1;
            Adj(1,startpos+whichone(i))=1;
        end
    end
    startpos=startpos+4;
    endpos=endpos+4;
end

degrees=sum(Adj,1);
lessthanfour=find(degrees<4); %compute all nodes with free links (i.e. <4 links)

sign=+1;
a=1;
while ~isempty(lessthanfour) %while there is still someone to be matched:
    partner=lessthanfour(a)+8*sign; %add (sign)8 to the position.
    if partner<1
        partner=N+partner; %if it goes below 0 i sum the number (which is negative in this case) from 24;
    end
    if ~isempty(find(lessthanfour==partner, 1)) % if the position has also less than 4 links
        pos_partner_vct=find(lessthanfour==partner, 1); % create 2 ways link
        Adj(lessthanfour(a),lessthanfour(pos_partner_vct))=1;
        Adj(lessthanfour(pos_partner_vct),lessthanfour(a))=1;
        toerase=[pos_partner_vct a];
        lessthanfour(toerase)=[]; %eliminate both from the list: first this because it should be after and  the current individual
        %lessthanfour(a)=[]; % 
    else % (if that position has already 4 links)
        sign=-sign; % invert sign
        partner=lessthanfour(a)+8*sign; 
        pos_partner_vct=find(lessthanfour==partner, 1); % create 2 ways link
        Adj(lessthanfour(a),lessthanfour(pos_partner_vct))=1;
        Adj(lessthanfour(pos_partner_vct),lessthanfour(a))=1;
        toerase=[pos_partner_vct a];
        lessthanfour(toerase)=[]; %eliminate both from the list: first this because it should be after
        %lessthanfour(a)=[]; % then the current individual   
    end
    sign=-(sign); % invert sign
end

degrees=sum(Adj,1);
lessthanfour=find(degrees<4); %compute all nodes with free links (i.e. <4 links)
a=1;
sign=-sign;
while ~isempty(lessthanfour) % Those that remail i connect by approsimation
    potentialpartner=lessthanfour(a)+8*sign; %add (sign)8 to the position.
    if potentialpartner<1
        potentialpartner=N+potentialpartner; %if it goes below 0 i sum the number (which is negative in this case) from 24;
    end    
    if isempty(find(lessthanfour==potentialpartner, 1)) 
        temp=lessthanfour; temp(a)=999999999;
        [~,posmin]=min(abs(potentialpartner-temp));
    end
    Adj(lessthanfour(a),lessthanfour(posmin))=1;
    Adj(lessthanfour(posmin),lessthanfour(a))=1;
    toerase=[a posmin];
    lessthanfour(toerase)=[];
    sign=-sign;
end


% adj2pajek(Adj,'lattice.net');
