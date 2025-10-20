# Automated Parameter Sweep Script
# Run multiple simulations with different configurations

Write-Host "=== Adventure World Parameter Sweep ===" -ForegroundColor Cyan
Write-Host ""

# Test 1: Small park
Write-Host "[Test 1] Small park with 3 rides..." -ForegroundColor Yellow
python adventureworld.py -f map1.csv -p params1.csv
Write-Host ""

# Test 2: Large park with more rides
Write-Host "[Test 2] Large park with 5 rides..." -ForegroundColor Yellow
python adventureworld.py -f map2.csv -p params2.csv
Write-Host ""

Write-Host "=== Parameter Sweep Complete ===" -ForegroundColor Green
