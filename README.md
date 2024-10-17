---
author:
- Ulrik Unneberg
title: Simply-Typed Lambda Calculus (STLC) with extensions
---

<!-- Use MathJax -->

# Introduction

This report presents the design and implementation of the **Simply-Typed
Lambda Calculus (STLC)** with extension to support for

-   Function types

-   Conjunctions

-   Disjunctions

-   Primitive types such as integers and booleans

-   Binary operation such as addition and multiplication and logical
    operations

-   Conditional expressions

-   Pairs and projections

-   Injections and cases

-   Simple proofs of propositional logic using the Curry-Howard
    Correspondence

This report explains the syntax, type rules, and evaluation rules of the
STLC, and is meant to be a reference for the implementation of the STLC
with extensions. Details of examples are found in the test notebook in
the repository.

# Syntax

We have the expressions in the STLC with as $$\begin{aligned}
    t &::= x \mid \lambda x: T. t \mid t_1 \ t_2 \mid \text{if } t_1 \ \text{then} \ t_2 \ \text{else} \ t_3 \\
      &\mid \langle t_1, t_2 \rangle \mid \text{fst}(t) \mid \text{snd}(t) \\
      &\mid \text{inl}_{A \lor B}(t) \mid \text{inr}_{A \lor B}(t) \mid \text{case } t \ \text{of} \ (\text{inl}_{A \lor B}(x) \Rightarrow t_1 \mid \text{inr}_{A \lor B}(y) \Rightarrow t_2),
\end{aligned}$$ and the types as $$\begin{aligned}
    T &::= \text{Int} \mid \text{Bool} \mid T_1 \to T_2 \mid T_1 \land T_2 \mid T_1 \lor T_2
\end{aligned}$$

# Type System

The type system of the STLC makes sure that all expressions are
well-typed, and is presented in the following.

## Function Types

$$\inferrule*[right=Abs]
    {\Gamma, x : A \vdash t : B}
    {\Gamma \vdash \lambda x: A. t : A \to B}$$

$$\inferrule*[right=App]
    {\Gamma \vdash t_1 : A \to B \quad \Gamma \vdash t_2 : A}
    {\Gamma \vdash t_1 \ t_2 : B}$$

## Conjunction Types

$$\inferrule*[right=Pair]
    {\Gamma \vdash t_1 : A \quad \Gamma \vdash t_2 : B}
    {\Gamma \vdash \langle t_1, t_2 \rangle : A \land B}$$

$$\inferrule*[right=Fst]
    {\Gamma \vdash t : A \land B}
    {\Gamma \vdash \text{fst}(t) : A}$$

$$\inferrule*[right=Snd]
    {\Gamma \vdash t : A \land B}
    {\Gamma \vdash \text{snd}(t) : B}$$

## Disjunction Types

$$\inferrule*[right=Inl]
    {\Gamma \vdash t : A}
    {\Gamma \vdash \text{inl}_{A \lor B}(t) : A \lor B}$$

$$\inferrule*[right=Inr]
    {\Gamma \vdash t : B}
    {\Gamma \vdash \text{inr}_{A \lor B}(t) : A \lor B}$$

$$\inferrule*[right=Case]
    {\Gamma \vdash t : A \lor B \quad \Gamma, x : A \vdash t_1 : C \quad \Gamma, y : B \vdash t_2 : C}
    {\Gamma \vdash \text{case } t \ \text{of} \ (\text{inl}_{A \lor B}(x) \Rightarrow t_1 \mid \text{inr}_{A \lor B}(y) \Rightarrow t_2) : C}$$

# Reduction rules

In these rules, we use the symbol $\rightsquigarrow$ to denote
evaluation. We distinguish between evaluation of terms (which can be
expressions like applications, pairs, etc.) and values (which are fully
evaluated results). For terms, the rules are evaluation of
sub-expressions, while for values, the rules are about substituting and
reducing the function body.

## Computation Rules

$$\frac{}
{\text{App}(\lambda x: A. t_1) \ t_2 \rightsquigarrow t_1[t_2 / x]} \quad \text{Eval-App}$$

$$\frac{}{\text{fst}(\langle v_1, v_2 \rangle) \rightsquigarrow v_1} \quad \text{Eval-Fst}$$

$$\frac{}{\text{snd}(\langle v_1, v_2 \rangle) \rightsquigarrow v_2} \quad \text{Eval-Snd}$$

$$\frac{
    e \rightsquigarrow e'
}{
    \text{Inl}(e) \to \text{Inl}(e')
} \quad \text{Eval-Inl}$$ $$\frac{
    e \rightsquigarrow e'
}{
    \text{Inr}(e) \to \text{Inr}(e')
} \quad \text{Eval-Inr}$$

$$\frac{}{\text{case} \ \text{Inl}(v) \ \text{of} \ (\text{Inl}(x) \Rightarrow t_1 \mid \text{Inr}(y) \Rightarrow t_2) \rightsquigarrow t_1[v / x]} \quad \text{Eval-Case-Inl}$$

$$\frac{}{\text{case} \ \text{Inr}(v) \ \text{of} \ (\text{Inl}(x) \Rightarrow t_1 \mid \text{Inr}(y) \Rightarrow t_2) \rightsquigarrow t_2[v / y]} \quad \text{Eval-Case-Inr}$$

$$\frac{}{\text{if true then} \ t_1 \ \text{else} \ t_2 \rightsquigarrow t_1} \quad \text{Eval-If-True}$$

$$\frac{}{\text{if false then} \ t_1 \ \text{else} \ t_2 \rightsquigarrow t_2} \quad \text{Eval-If-False}$$

## Congruence Rules

$$\frac{e_1 \rightsquigarrow e_1'}{\text{App}(e_1, e_2) \rightsquigarrow \text{App}(e_1', e_2)} \quad \text{Eval-Rator}$$

$$\frac{e_2 \rightsquigarrow e_2'}{\text{App}(v_1, e_2) \rightsquigarrow \text{App}(v_1, e_2')} \quad \text{Eval-Rand}$$

$$\frac{e_1 \rightsquigarrow e_1'}{\text{fst}(e_1) \rightsquigarrow \text{fst}(e_1')} \quad \text{Cong-Fst}$$

$$\frac{e_1 \rightsquigarrow e_1'}{\text{snd}(e_1) \rightsquigarrow \text{snd}(e_1')} \quad \text{Cong-Snd}$$

$$\frac{e_1 \rightsquigarrow e_1'}{\text{case} \ e_1 \ \text{of} \ (\text{Inl}(x) \Rightarrow t_1 \mid \text{Inr}(y) \Rightarrow t_2) \rightsquigarrow \text{case} \ e_1' \ \text{of} \ (\text{Inl}(x) \Rightarrow t_1 \mid \text{Inr}(y) \Rightarrow t_2)} \quad \text{Cong-Case}$$

$$\frac{e_1 \rightsquigarrow e_1'}{\langle e_1, e_2 \rangle \rightsquigarrow \langle e_1', e_2 \rangle} \quad \text{Cong-Pair-Left}$$

$$\frac{e_2 \rightsquigarrow e_2'}{\langle v_1, e_2 \rangle \rightsquigarrow \langle v_1, e_2' \rangle} \quad \text{Cong-Pair-Right}$$

$$\frac{e_1 \rightsquigarrow e_1'}{\text{if} \ e_1 \ \text{then} \ e_2 \ \text{else} \ e_3 \rightsquigarrow \text{if} \ e_1' \ \text{then} \ e_2 \ \text{else} \ e_3} \quad \text{Cong-If}$$

$$\frac{e_1 \rightsquigarrow e_2}{\lambda(x : \tau_1). e_1 \rightsquigarrow \lambda(x : \tau_1). e_2} \quad \text{Eval-$\lambda$-Body}$$

# Examples (also given in test notebook in repo)

In the notebook, we will demonstrate that binary operations such as
addition and multiplication, and logical operations such as conjunction
and disjunction, and conditional (if) statements, can be implemented
using our STLC with extensions. We will also show how to implement
conditional expressions, pairs and projections, injections and cases,
and simple proofs of propositional logic using the Curry-Howard
Correspondence. Some proof we will go through is the following

## Proof: $(A \land B) \to A$

$$\lambda p: A \land B. \ \text{fst}(p)$$

## Proof: $A \to (A \lor B)$

$$\lambda a: A. \ \text{inl}_{A \lor B}(a)$$

## Proof: $(A \to C) \land (B \to C) \to (A \lor B \to C)$

$$\lambda f: (A \to C) \land (B \to C). \ \lambda x: A \lor B. \ 
\text{case } x \ \text{of} \ (\text{inl}_{A \lor B}(a) \Rightarrow \text{fst}(f)(a) \mid \text{inr}_{A \lor B}(b) \Rightarrow \text{snd}(f)(b))$$
