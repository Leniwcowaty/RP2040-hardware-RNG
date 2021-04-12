clear;
pkg load communications;
data_raw = load('rng_data_60C_Laptop.txt');

fid_raw = fopen('data_raw_60C.bin','w');
fwrite (fid_raw, data_raw,'uint16');
fclose (fid_raw);

fid_raw = fopen('data_raw_60C.bin','r');
data8_raw = fread (fid_raw, 100000, 'uint8');
fclose (fid_raw);

data_final = load('final_data_60C_Laptop.txt');

fid_final = fopen('data_final_60C.bin','w');
fwrite (fid_final, data_final,'uint32');
fclose (fid_final);

fid_final = fopen('data_final_60C.bin','r');
data8_final = fread (fid_final, 4000000, 'uint8');
fclose (fid_final);

a=data8_raw;
b=data8_final;
n = 8;
m = 2^n-1;

subplot(2,1,1)
hist(a,m);
subplot(2,1,2)
hist(b,m);

[NN,XX]=hist(a,m);
[MM,YY]=hist(b,m);
NN = NN+1;
MM = MM+1;
p_raw=NN/sum(NN); 
p_final=MM/sum(MM);
ent_raw = -sum(p_raw.*log2(p_raw)) 
ent_final = -sum(p_final.*log2(p_final))