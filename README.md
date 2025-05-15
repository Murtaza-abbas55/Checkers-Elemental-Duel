# Checkers-Elemental-Duel

The project focuses on creating a strategic and adaptive AI opponent for Checkers: Elemental Duel, a variant of traditional Checkers where each piece has an elemental affinity (e.g., fire, water, earth, air). The game introduces a rock-paper-scissors mechanic for piece interactions, adding a layer of complexity and strategy to the classic game.

# Video Demo

https://github.com/user-attachments/assets/72c39a34-b3ad-4cfd-8d8c-8554fee1d7aa

# Project Report

**Course**: AI  
**Submitted By**:

-   Uzair Khan (22K-4344)
-   Zeefan Manzoor (22K-4650)
-   Murtaza Abbas (22K-4368)

**Instructors**: Miss Alina Arshad, Miss Syeda Ravia Ejaz  
**Submission Date**: 15 May 2025

---

## 1. Executive Summary

### Project Overview

This project reimagines the classic Checkers game by introducing elemental properties (Fire, Water, Earth, Air) to each piece and integrating an AI opponent that makes strategic decisions using the Minimax algorithm with Alpha-Beta pruning. The primary objective is to enhance traditional Checkers with thematic gameplay mechanics and build a competent AI to challenge human players.

---

## 2. Introduction

### Background

Checkers is a two-player strategy board game ideal for AI experimentation due to its well-defined rules. In **Checkers: Elemental Duel**, each piece has an elemental type, introducing a rock-paper-scissors-like mechanic that influences move options and combat outcomes.

### Objectives

-   Modify traditional Checkers with elemental dynamics.
-   Implement AI using Minimax with Alpha-Beta pruning.
-   Evaluate AI's strategic effectiveness against human players.

---

## 3. Game Description

### Original Game Rules

-   12 pieces per player.
-   Diagonal forward movement.
-   Jump to capture.
-   Kings move both directions after reaching the opponent’s back row.

### Innovations and Modifications

-   Elements: Fire, Water, Earth, Air.
-   Elemental advantage system (e.g., Fire beats Air).
-   Capturing allowed only with neutral or advantageous elements.
-   AI opponent with Minimax + Alpha-Beta pruning.

---

## 4. AI Approach and Methodology

### Techniques Used

Minimax algorithm with Alpha-Beta pruning for strategic decision-making.

### Heuristic Design

-   Evaluates piece count, king status, and elemental advantage.
-   Higher weights for kings.
-   Elemental strengths factored in.

### Performance Evaluation

-   Average response time: **< 1 second/move**.
-   Win rate: **100% vs human players**.

---

## 5. Game Mechanics and Rules

### Modified Rules

-   Random elemental assignment at start.
-   Capture allowed only when attacker has neutral or better elemental status.
-   Standard movement retained.

### Turn-Based Mechanics

-   Players alternate turns.
-   Human: White pieces; AI: Black pieces.
-   Moves include standard movement or jumps based on valid paths.

### Winning Conditions

-   Eliminate all opponent pieces, or block all their valid moves.

---

## 6. Implementation and Development

### Development Process

-   Game logic and UI built using Python and Pygame.
-   Minimax algorithm implemented for AI.
-   Integrated user input and win/loss conditions.

### Tools & Technologies

-   **Language**: Python
-   **Libraries**: Pygame, NumPy
-   **IDE**: Visual Studio Code

### Challenges

-   Balancing elemental interactions.
-   Optimizing Minimax depth.
-   Synchronizing AI and player turns.

---

## 7. Team Contributions

-   **Uzair Khan**: Developed and optimized AI (Minimax + heuristics).
-   **Zeefan Manzoor**: Designed elemental system and balanced gameplay.
-   **Murtaza Abbas**: Built the game interface and managed user input.

---

## 8. Results and Discussion

-   **AI Win Rate**: 100% vs human players.
-   **Avg. Decision Time**: < 1 second.
-   **Strategic Behavior**: Strong use of elemental tactics and board control.
-   **Gameplay Impact**: Elemental rules introduced strategic depth and variety.

---

## 9. References

-   [Pygame Documentation](https://www.pygame.org/docs/)
-   [Alpha-Beta Pruning - GeeksforGeeks](https://www.geeksforgeeks.org/alpha-beta-pruning/)
-   [NumPy Documentation](https://numpy.org/doc/)
