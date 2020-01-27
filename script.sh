echo "Iniciando testes sem busca Local"

python3 main_semBusca.py < md-12-966.in > md12966_semBusca.out
python3 main_semBusca.py < SJC1.dat > SJC1_semBusca.out
python3 main_semBusca.py < SJC2.dat > SJC2_semBusca.out
python3 main_semBusca.py < SJC3a.dat > SJC3a_semBusca.out
python3 main_semBusca.py < SJC3b.dat > SJC3b_semBusca.out
python3 main_semBusca.py < SJC4a.dat > SJC4a_semBusca.out
python3 main_semBusca.py < SJC4b.dat > SJC4b_semBusca.out

echo "Iniciando testes com busca Local"

python3 main.py < md-12-966.in > md12966.out
python3 main.py < SJC1.dat > SJC1.out
python3 main.py < SJC2.dat > SJC2.out
python3 main.py < SJC3a.dat > SJC3a.out
python3 main.py < SJC3b.dat > SJC3b.out
python3 main.py < SJC4a.dat > SJC4a.out
python3 main.py < SJC4b.dat > SJC4b.out

echo "Testes finalizados"