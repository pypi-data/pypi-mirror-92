## bodas

![](https://github.com/urbanij/bodas/blob/main/docs/example1.png?raw=true)

### Installation
`pip install bodas`


### Basic usage
```python
import bodas
import sympy

s = sympy.Symbol('s')

H = 1/(1 + s/120)

bodas.plot( str(H) )
```
