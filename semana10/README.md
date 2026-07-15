# Exercicios C


### Olá mundo


```c
#include <stdio.h>

int main(void) {
    printf("Ola, mundo!\n");
    return 0;
}
```
---


### Inspecionando tamanhos

```c
#include <stdio.h>

int main(void) {
    printf("char:   %zu byte(s)\n", sizeof(char));
    printf("int:    %zu byte(s)\n", sizeof(int));
    printf("long:   %zu byte(s)\n", sizeof(long));
    printf("float:  %zu byte(s)\n", sizeof(float));
    printf("double: %zu byte(s)\n", sizeof(double));
    return 0;
}
```

---

### variável não inicializada vs. inicializada

```c
#include <stdio.h>

int main(void) {
    int a = 42;
    int b;         
    b = a + 8;
    printf("a = %d\n", a);
    printf("b = %d\n", b);

    const int N = 100;
    N = 200;
    printf("N = %d\n", N);
    return 0;
}
```
---


### Divisão inteira, módulo e incremento

```c
#include <stdio.h>

int main(void) {
    int a = 17, b = 5;

    printf("%d / %d = %d\n", a, b, a / b);  /* divisao inteira */
    printf("%d %% %d = %d\n", a, b, a % b); /* resto */

    int x = 3;
    int pre  = ++x;   /* x vira 4, pre  = 4 */
    int pos  = x++;   /* pos = 4, x  vira 5 */
    printf("pre=%d  pos=%d  x=%d\n", pre, pos, x);

    int max = (a > b) ? a : b;
    printf("max(%d,%d) = %d\n", a, b, max);
    return 0;
}
```

---


###  if / else if / else

```c
#include <stdio.h>

int main(void) {
    int nota = 72;

    if      (nota >= 90) printf("A\n");
    else if (nota >= 80) printf("B\n");
    else if (nota >= 70) printf("C\n");
    else                 printf("Reprovado\n");

    return 0;
}
```

---

### for com break e continue

```c
#include <stdio.h>

int main(void) {
    for (int i = 0; i < 10; i++) {
        if (i % 2 == 0) continue; /* pula pares */
        if (i == 7)     break;    /* para no 7  */
        printf("%d\n", i);
    }
    return 0;
}
```

---

### do-while

```c
#include <stdio.h>

int main(void) {
    int n = 1;
    do {
        printf("n = %d\n", n);
        n *= 2;
    } while (n < 32);
    return 0;
}
```

---

### switch com fall-through

```c
#include <stdio.h>

int main(void) {
    int dia = 3;   /* 1=Seg ... 7=Dom */

    switch (dia) {
        case 1: case 2: case 3: case 4: case 5:
            printf("Dia util\n");
            break;
        case 6: case 7:
            printf("Fim de semana\n");
            break;
        default:
            printf("Invalido\n");
    }
    return 0;
}
```
---


### pilha de chamadas em ação

```c
#include <stdio.h>

int fatorial(int n) {
    if (n <= 1) return 1;
    return n * fatorial(n - 1);  /* chamada recursiva */
}

void dobra(int *x) { *x *= 2; }

int main(void) {
    int f = fatorial(5);
    printf("5! = %d\n", f);

    int v = 7;
    dobra(&v);
    printf("dobro de 7 = %d\n", v);
    return 0;
}
```
---


###  Array unidimensional e matriz

```c
#include <stdio.h>

int main(void) {
    int v[5] = {10, 20, 30, 40, 50};

    /* soma dos elementos */
    int soma = 0;
    for (int i = 0; i < 5; i++)
        soma += v[i];
    printf("soma = %d\n", soma);

    /* matriz 2x3 */
    int m[2][3] = {{1, 2, 3}, {4, 5, 6}};
    printf("m[1][2] = %d\n", m[1][2]);  /* 6 */
    return 0;
}
```

---

### Percorrendo uma string caractere a caractere

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char s[] = "Brasilia";
    int  len = strlen(s);

    printf("Comprimento: %d\n", len);

    /* percorre e imprime cada char e seu codigo ASCII */
    for (int i = 0; i < len; i++)
        printf("s[%d] = '%c'  (ASCII %d)\n", i, s[i], s[i]);

    /* comparacao */
    char t[] = "Brasilia";
    printf("strcmp: %d\n", strcmp(s, t));  /* 0 = iguais */
    return 0;
}
```

---


###  Ponteiro básico e de referência

```c
#include <stdio.h>

int main(void) {
    int x = 10;
    int *p = &x;

    printf("x    = %d\n",  x);
    printf("&x   = %p\n",  (void*)&x);
    printf("p    = %p\n",  (void*)p);
    printf("*p   = %d\n",  *p);

    *p = 99;
    printf("x apos *p=99: %d\n", x);
    return 0;
}
```
---

### Aritmética de ponteiros e equivalência com índice

```c
#include <stdio.h>

int main(void) {
    int v[4] = {10, 20, 30, 40};
    int *p = v;          /* p aponta para v[0] */

    printf("*p      = %d\n", *p);       /* 10 */
    printf("*(p+1)  = %d\n", *(p+1));  /* 20 */
    printf("*(p+2)  = %d\n", *(p+2));  /* 30 */

    p++;                 /* agora aponta para v[1] */
    printf("apos p++: *p = %d\n", *p); /* 20 */
    return 0;
}
```

---

###  Ponteiro para ponteiro

```c
#include <stdio.h>

int main(void) {
    int  x  = 42;
    int *p  = &x;
    int **pp = &p;

    printf("x   = %d\n",   x);
    printf("*p  = %d\n",  *p);
    printf("**pp= %d\n", **pp);

    **pp = 100;           /* altera x via dois níveis de indireção */
    printf("x apos **pp=100: %d\n", x);
    return 0;
}
```
---

### Heap vs Stack

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n = 4;
    int *v = malloc(n * sizeof(int));  /* aloca no heap */

    for (int i = 0; i < n; i++)
        v[i] = (i + 1) * 10;          /* 10 20 30 40 */

    for (int i = 0; i < n; i++)
        printf("v[%d] = %d\n", i, v[i]);

    free(v);    /* devolve ao heap */
    v = NULL;   /* evita uso acidental */
    return 0;
}
```
---

### Struct com acesso direto e via ponteiro

```c
#include <stdio.h>

typedef struct {
    int x;
    int y;
} Ponto;

float distancia(Ponto *a, Ponto *b) {
    int dx = a->x - b->x;
    int dy = a->y - b->y;
    /* evitamos sqrt para simplificar */
    return (float)(dx*dx + dy*dy);
}

int main(void) {
    Ponto origem = {0, 0};
    Ponto p      = {3, 4};

    printf("p.x=%d  p.y=%d\n", p.x, p.y);

    Ponto *ptr = &p;
    ptr->x = 10;
    printf("apos ptr->x=10: p.x=%d\n", p.x);

    printf("dist^2(origem,p) = %.0f\n", distancia(&origem, &p));
    return 0;
}
```
---

### Union: membros compartilham memória

```c
#include <stdio.h>

union Dado {
    int   i;
    float f;
    char  c;
};

int main(void) {
    union Dado d;
    d.i = 65;
    printf("d.i = %d\n",   d.i);
    printf("d.c = '%c'\n", d.c);  /* mesmo bytes, interpretado como char */
    d.f = 3.14f;
    printf("d.f = %.2f\n", d.f);
    /* d.i agora tem valor indefinido (sobrescrito por f) */
    return 0;
}
```

### enum com switch

```c
#include <stdio.h>

typedef enum { DOM=0, SEG, TER, QUA, QUI, SEX, SAB } DiaSemana;

const char *nome_dia(DiaSemana d) {
    switch (d) {
        case DOM: return "Domingo";
        case SEG: return "Segunda";
        case TER: return "Terca";
        case QUA: return "Quarta";
        case QUI: return "Quinta";
        case SEX: return "Sexta";
        case SAB: return "Sabado";
        default:  return "???";
    }
}

int main(void) {
    for (DiaSemana d = DOM; d <= SAB; d++)
        printf("%d = %s\n", d, nome_dia(d));
    return 0;
}
```
---

### Formatação de saída 

```c
#include <stdio.h>

int main(void) {
    int    i = 255;
    float  f = 3.14159f;
    char   c = 'Z';
    char   s[] = "Brasilia";

    printf("Decimal:     %d\n",   i);
    printf("Hexadecimal: %x\n",   i);   /* ff */
    printf("Float 2dec:  %.2f\n", f);
    printf("Char:        %c\n",   c);
    printf("String:      %s\n",   s);
    printf("Ponteiro:    %p\n",   (void*)s);
    return 0;
}
```
---

### constante e macro com parâmetro

```c
#include <stdio.h>

#define PI        3.14159
#define QUADRADO(x) ((x)*(x))
#define MAX(a,b)  ((a)>(b)?(a):(b))

int main(void) {
    double r = 5.0;
    printf("Area do circulo r=5: %.2f\n", PI * QUADRADO(r));

    int a = 7, b = 3;
    printf("MAX(%d,%d) = %d\n", a, b, MAX(a,b));

    /* armadilha classica de macro sem parenteses */
    printf("QUADRADO(a+1) = %d\n", QUADRADO(a+1)); /* (a+1)*(a+1) = 64 */
    return 0;
}
```
---

### Escopo de bloco

```c
#include <stdio.h>

int main(void) {
    int x = 1;
    printf("x externo = %d\n", x);

    {
        int x = 2;   /* nova variavel, esconde a externa */
        printf("x interno = %d\n", x);
    }

    printf("x externo apos bloco = %d\n", x);  /* ainda 1 */
    return 0;
}
```
---

### Variável `static` local

```c
#include <stdio.h>

void contador(void) {
    static int n = 0;   /* inicializado UMA VEZ; persiste */
    n++;
    printf("chamada numero %d\n", n);
}

int main(void) {
    contador();  /* 1 */
    contador();  /* 2 */
    contador();  /* 3 */
    return 0;
}
```

### Detectando estouro de buffer

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char destino[8];

    /* SEGURO: limita a copia ao tamanho do buffer */
    strncpy(destino, "Brasilia-DF", sizeof(destino) - 1);
    destino[sizeof(destino) - 1] = '\0';   /* garante terminador */

    printf("destino = '%s'\n", destino);
    printf("strlen  = %zu\n",  strlen(destino));
    return 0;
}
```