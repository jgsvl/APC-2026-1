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
