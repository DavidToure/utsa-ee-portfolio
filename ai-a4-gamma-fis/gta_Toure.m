%% gamma_threat_analysis
% EE 5663 Artificial Intelligence - Assignment 4, Problem 4
% Fuzzy inference system for gamma-ray spectrum threat-confidence scoring.
% David Toure

clear; clc; close all;

scenario_files = {'Scenario1.txt','Scenario2.txt','Scenario3.txt', ...
                   'Scenario4.txt','Scenario5.txt'};
N = numel(scenario_files);

NTOTAL = zeros(N,1);
MAX8   = zeros(N,1);
BIN05  = zeros(N,1);
BIN08  = zeros(N,1);

figure('Name','Raw gamma-ray spectra');
for k = 1:N
    data = load(scenario_files{k});           % 1024x1 vector of counts

    % Step 2: plot the raw spectrum
    subplot(N,1,k);
    plot(data); xlabel('Bin'); ylabel('Counts');
    title(sprintf('%s (raw)', scenario_files{k}), 'Interpreter','none');

    % Step 3: normalize by the spectrum's own maximum
    norm_data = data / max(data);

    % Step 4a: NTOTAL = sum of all normalized counts
    NTOTAL(k) = sum(norm_data);

    % Step 4b: MAX8 = max over the LAST 800 of the 1024 bins 
    last800 = norm_data(end-799:end);          % bins 225-1024
    MAX8(k) = max(last800);

    % Step 5a: BIN05 = count of bins with normalized value < 0.5 
    BIN05(k) = sum(norm_data < 0.5);

    % Step 5b: BIN08 = count of bins with normalized value > 0.8 
    BIN08(k) = sum(norm_data > 0.8);
end

T = table((1:N)', NTOTAL, MAX8, BIN05, BIN08, ...
    'VariableNames', {'Scenario','NTOTAL','MAX8','BIN05','BIN08'});
disp(T);

%% ---- Step 6: evaluate the fuzzy inference system ----
fis_name = 'gamma_threat_fis.fis';
if exist(fis_name, 'file') ~= 2
    % not in the current folder -- try the folder this script lives in
    here = fileparts(mfilename('fullpath'));
    if ~isempty(here) && exist(fullfile(here, fis_name), 'file') == 2
        fis_name = fullfile(here, fis_name);
    else
        error(['Cannot find %s in MATLAB''s current folder:\n  %s\n' ...
               'Put gamma_threat_fis.fis there (if it downloaded as ' ...
               '"gamma_threat_fis (1).fis", rename it).'], fis_name, pwd);
    end
end
temp = readfis(fis_name);                      % load the Mamdani FIS
inputdata = [NTOTAL, MAX8, BIN05, BIN08];      % column order must match
                                                % the FIS's Input1..Input4
Conf = evalfis(temp, inputdata);               % Conf is in [0 100] (%)

for k = 1:N
    fprintf('%s : NTOTAL=%.2f  MAX8=%.4f  BIN05=%d  BIN08=%d  ->  Threat confidence = %.2f%%\n', ...
        scenario_files{k}, NTOTAL(k), MAX8(k), BIN05(k), BIN08(k), Conf(k));
end

figure('Name','Threat confidence per scenario');
bar(Conf);
set(gca,'XTickLabel',{'S1','S2','S3','S4','S5'});
ylabel('Threat confidence (%)');
title('Gamma-ray spectrum threat confidence (fuzzy inference output)');
ylim([0 100]);
%% figure 4.2 
figure('Name','Fig 4.2 - Input fuzzy sets');
for i = 1:4
    subplot(2,2,i);
    plotmf(temp,'input',i);
    title(temp.Inputs(i).Name);
end
