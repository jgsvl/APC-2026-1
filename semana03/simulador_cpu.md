# Semana 3
Programa que, dado a entrada do usuário, retorna uma lista de números inteiros naturais, de zero até o número definido pelo usuário.  
Este programa roda nos simuldores LMC (Little Man Computer).

```asm
        INP
        STA limite     
loop    LDA atual
        OUT   
        ADD um
        STA atual
        LDA limite
        SUB um
        STA limite
        BRP loop
        HLT

atual DAT 0
um DAT 1
limite DAT
```
