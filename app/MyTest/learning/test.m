[c,g] = meshgrid(-10:0.2:10,-10:0.5:10);
[m,n] = size(c);
cg = zeros(m,n);
eps = 10^(-4);
v = 5;
bestc = 1;
bestg = 0.1;
bestacc = 0;
for i = 1:m
    for j = n:n
        cmd = ['-v ',num2str(v),' -t 2',' -c ',num2str(2^c(i,j)),' -g ',num2str(2^g(i,j)),' -s 2', ' -n 0.5'];
        cg(i,j) = svmtrain(trainLabel,trainMatrix,cmd);
        if cg(i,j) > bestacc
            bestacc = cg(i,j);
            bestc = 2^c(i,j);
            bestg = 2^g(i,j);
        end
        if abs( cg(i,j)-bestacc )<=eps && bestc > 2^c(i,j)
            bestacc = cg(i,j);
            bestc = 2^c(i,j);
            bestg = 2^g(i,j);
        end
    end
end

cmd = [' -t 2',' -c ',num2str(bestc),' -g ',num2str(bestg),' -n 0.5',' -s 2'];
model = svmtrain(trainLabel,trainMatrix,cmd);