# 🌌 Cosmos: O Pálido Ponto Azul

An interactive and reflective 2D space arcade game developed in Python using the **Pygame** library. This project was built as a practical assignment for the Applied Programming Language course (UNINTER, 2026).

The game combines classic *Shoot 'em up* mechanics with deep philosophical narrative transitions inspired by Carl Sagan's book, *Pale Blue Dot*, culminating in a personalized, interactive ending.

---

> <details>
> <summary> Veja aqui o jogo e as fases</summary>
> 
> ![img1](https://github.com/jaiane-soares/cosmos/blob/main/cosmosUm.png)
> 
> ![img1](https://github.com/jaiane-soares/cosmos/blob/main/cosmosDois.png)
>  
> ![img1](https://github.com/jaiane-soares/cosmos/blob/main/cosmosTres.png)
>  
> ![img1](https://github.com/jaiane-soares/cosmos/blob/main/CosmosQuatro.png)
>  
> ![img1](https://github.com/jaiane-soares/cosmos/blob/main/CosmosCinco.png)
>
> </details>

##  Project requirements (UNINTER)

This project strictly adheres to all evaluation criteria required by the institution:
* **2D Graphical Interface:** Built entirely outside the OS command line/console.
* **Main Menu:** Includes an accessible user interface displaying core inputs before starting.
* **Gameplay Loop:** Features active player controls, adaptive challenges (asteroids & alien drones), a win state, and a lose state.
* **Relative Paths:** Strictly uses relative asset paths to ensure multi-platform compatibility and prevent execution failures during grading.
* **Windows Build Compilation:** Structured and optimized to support compilation into a standard Windows standalone executable (`.exe`).

---

##  Mechanics & Features

* **Sector Progression (Levels):** The game is divided into 4 cosmic sectors. To bypass a sector, the player must score points by neutralizing orbital debris.
* **Adaptive Difficulty:** As sectors progress, asteroids drop down faster, and tactical alien probes spawn at the top, firing back at the player.
* **Lore Integration:** Breaking score thresholds unlocks real historical reflections about our planet's fragility in the cosmos.
* **Interactive Secret Ending:** Upon completion, the player encounters the *Cosmic Engineer Jai* spacecraft. Clicking directly on the ship decrypts a final encrypted galactic transmission.

---

## Controls

* **Left / Right Arrow Keys:** Navigation & lateral movement.
* **Spacebar:** Discharges forward laser matrix modules.
* **Mouse Left-Click:** Interacts with anomalous space entities on the victory screen.
* **ENTER:** Confirms selections, boots up systems, and skips sector transition screens.
* **M Key:** Reboots the program back to the Main Menu (available on Game Over / Victory screens).

---

##  Tech Stack & Architecture

* **Language:** Python
* **Engine/Library:** Pygame
* **Design Pattern:** State Machine Architecture (`MENU`, `JOGO`, `TRANSIÇÃO`, `VITORIA`, `DERROTA`)
* **Visuals:** Native procedurally generated vector polygons and automated particle stars.
* **Typography:** System-agnostic fallback styling via standard Windows fonts (`Consolas` and `Georgia`) to maintain visual layout integrity.

---

## Author

Developed by **Jaiane (Jai)** – Software Engineering Student.  
*Academic project supervised by Prof. Jadson de Araujo Almeida.*
