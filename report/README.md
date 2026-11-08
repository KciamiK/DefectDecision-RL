Dokumentacja projektu DefectDecision-RL w LaTeX.

---

## Implementacja etapu E2

Projekt DefectDecision-RL jest symulatorem przemysłowej kontroli
jakości aluminiowych płytek wykorzystującym uczenie ze wzmocnieniem.

### Zaimplementowane funkcjonalności

- Generator partii 10 aluminiowych płytek.
- Cztery rodzaje nieprawidłowości: rysy, pęknięcia,
  błędy otworów montażowych i korozja.
- Reguły określające rzeczywistą jakość produktu.
- Podstawowy skaner z prawdopodobieństwem błędu 25%.
- Szczegółowy skaner z prawdopodobieństwem błędu 5%.
- Środowisko RL z metodami reset() i step().
- Akcje ACCEPT, REJECT oraz INSPECT.
- Budżet 4 dodatkowych kontroli na partię.
- Agent losowy i agent heurystyczny.
- Eksperymenty porównawcze oraz zapis wyników CSV.
- Automatyczne testy środowiska.

Obecne skanery wykorzystują statystyczną symulację błędów
pomiarowych. Analiza syntetycznych obrazów 2D oraz algorytm
Q-learning są zaplanowane na kolejny etap projektu.

### Wymagania

- Python 3.12
- Biblioteki wymienione w requirements.txt

### Instalacja na Windows

Sklonuj repozytorium:

```powershell
git clone https://github.com/KciamiK/DefectDecision-RL.git
cd DefectDecision-RL
```

Utwórz środowisko wirtualne:

```powershell
py -3.12 -m venv .venv
```

Aktywuj środowisko:

```powershell
.\.venv\Scripts\Activate.ps1
```

Jeśli PowerShell blokuje aktywację, w bieżącej sesji
można wykonać:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Zainstaluj biblioteki:

```powershell
python -m pip install -r requirements.txt
```

### Uruchamianie programu

Demonstracja środowiska RL:

```powershell
python src\quality_env.py
```

Agent losowy:

```powershell
python src\random_agent.py
```

Agent heurystyczny:

```powershell
python src\heuristic_agent.py
```

### Eksperymenty porównawcze

Aby porównać obu agentów na 1000 epizodów
dla każdej strategii:

```powershell
python experiments\compare_baselines.py
```

Wyniki są zapisywane w katalogu results:

- baseline_episodes.csv - wyniki pojedynczych epizodów.
- baseline_summary.csv - podsumowanie obu strategii.

### Testy automatyczne

Uruchomienie wszystkich testów:

```powershell
python -m pytest tests -v
```

W etapie E2 przygotowano 18 przypadków testowych,
które zakończyły się pomyślnie.

### Powtarzalność eksperymentów

Eksperymenty wykorzystują ustalone ziarna losowe.
Pozwala to odtwarzać wyniki oraz porównywać agentów
na identycznych partiach produktów.

### Dalszy rozwój

W etapie E3 planowane są:

- Implementacja tablicowego algorytmu Q-learning.
- Trening i ewaluacja agenta uczącego się.
- Porównanie Q-learningu z agentami bazowymi.
- Generowanie syntetycznych obrazów aluminiowych płytek.
- Implementacja prostego skanera obrazów.
- Wizualizacja procesu kontroli jakości w Pygame.
- Wykresy uczenia i końcowa analiza wyników.
