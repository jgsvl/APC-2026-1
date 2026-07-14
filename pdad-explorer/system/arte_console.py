def imprime_banner():
    """Imprime o banner do sistema no console."""
    # O "r" antes da string indica que é uma raw string, então 
    # não precisamos escapar as barras invertidas.
    print(r"""
     ____.                       ________      ___.         .__       .__   
    |    | _________    ____    /  _____/_____ \_ |_________|__| ____ |  |  
    |    |/  _ \__  \  /  _ \  /   \  ___\__  \ | __ \_  __ \  |/ __ \|  |  
/\__|    (  <_> ) __ \(  <_> ) \    \_\  \/ __ \| \_\ \  | \/  \  ___/|  |__
\________|\____(____  /\____/   \______  (____  /___  /__|  |__|\___  >____/
                    \/                 \/     \/    \/              \/       
    """)