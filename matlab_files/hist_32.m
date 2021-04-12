clear;
data_raw = load('rng_data_21C_Laptop.txt');
data_final = load('final_data_21C_Laptop.txt');

subplot(2,1,1)
  hist(data_raw, 100)
subplot(2,1,2)
  hist(data_final, 100)