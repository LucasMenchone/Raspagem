import subprocess
import os

def main():
    base_dir = os.path.dirname(__file__)

    raspagem_path = os.path.join(base_dir, "raspagem.py")
    medianas_path = os.path.join(base_dir, "medianas.py")

    python_path = os.path.join(base_dir, "../env/Scripts/python.exe")
    
    print("Executando raspagem de dados...")
    subprocess.run([python_path, raspagem_path], check=True)
    print("Raspagem concluída!")

    print("Calculando medianas...")
    subprocess.run([python_path, medianas_path], check=True)
    print("Cálculo das medianas concluído!")

if __name__ == "__main__":
    main()
