import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import requests
import os
import threading

# --- PALETA NORD ---
NORD = {
    "bg_dark": "#2E3440",        # Fondo principal de la ventana
    "bg_widget": "#3B4252",      # Fondo de widgets (entry, frame)
    "bg_entry": "#434C5E",       # Fondo de campos de texto
    "border": "#4C566A",         # Bordes y separadores
    "fg_primary": "#D8DEE9",     # Texto principal
    "fg_secondary": "#E5E9F0",   # Texto secundario (más claro)
    "fg_dim": "#9BA5B5",         # Texto tenue (para estados)
    "green": "#A3BE8C",          # Verde (éxito)
    "blue": "#81A1C1",           # Azul (info)
    "blue_dark": "#5E81AC",      # Azul oscuro (hover)
    "red": "#BF616A",            # Rojo (error)
    "orange": "#D08770",         # Naranja (advertencia)
}

class Descargador:
    def __init__(self, root):
        self.root = root
        self.root.title("Descargador de imágenes")
        self.root.resizable(False, False)
        
        # Aplicar fondo Nord a la ventana principal
        self.root.configure(bg=NORD["bg_dark"])
        
        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 12, "pady": 6}
        
        # --- Estilo para ttk (botones, progressbar) ---
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para Progressbar
        style.configure("Nord.Horizontal.TProgressbar",
                        background=NORD["blue"],
                        troughcolor=NORD["bg_widget"],
                        bordercolor=NORD["border"],
                        lightcolor=NORD["blue"],
                        darkcolor=NORD["blue_dark"])
        
        # Estilo para botones ttk (por si los usamos)
        style.configure("Nord.TButton",
                        background=NORD["blue"],
                        foreground=NORD["bg_dark"],
                        borderwidth=1,
                        padding=6)
        style.map("Nord.TButton",
                  background=[('active', NORD["blue_dark"])])

        # --- Configurar estilo de Labels ---
        label_style = {"bg": NORD["bg_dark"], "fg": NORD["fg_secondary"]}
        entry_style = {
            "bg": NORD["bg_entry"],
            "fg": NORD["fg_primary"],
            "insertbackground": NORD["fg_primary"],
            "relief": "flat",
            "highlightthickness": 2,
            "highlightcolor": NORD["blue"],
            "highlightbackground": NORD["border"]
        }
        button_style = {
            "bg": NORD["blue"],
            "fg": NORD["bg_dark"],
            "activebackground": NORD["blue_dark"],
            "activeforeground": NORD["fg_secondary"],
            "relief": "raised",
            "borderwidth": 2,
            "cursor": "hand2"
        }

        # --- Archivo CSV ---
        tk.Label(self.root, text="Archivo CSV:", **label_style).grid(row=0, column=0, sticky="w", **pad)
        
        self.csv_var = tk.StringVar(value="links.csv")
        tk.Entry(self.root, textvariable=self.csv_var, width=45, state="readonly", **entry_style).grid(row=0, column=1, **pad)
        
        btn_seleccionar = tk.Button(self.root, text="📂 Seleccionar…", command=self._elegir_csv, **button_style)
        btn_seleccionar.grid(row=0, column=2, **pad)

        # --- Carpeta de destino ---
        tk.Label(self.root, text="Carpeta de destino:", **label_style).grid(row=1, column=0, sticky="w", **pad)
        
        self.dest_var = tk.StringVar(value="Imgs")
        tk.Entry(self.root, textvariable=self.dest_var, width=45, state="readonly", **entry_style).grid(row=1, column=1, **pad)
        
        btn_cambiar = tk.Button(self.root, text="📁 Cambiar…", command=self._elegir_dest, **button_style)
        btn_cambiar.grid(row=1, column=2, **pad)

        # --- Barra de progreso ---
        self.progreso = ttk.Progressbar(self.root, length=400, mode="determinate", style="Nord.Horizontal.TProgressbar")
        self.progreso.grid(row=2, column=0, columnspan=3, **pad)

        # --- Etiqueta de estado ---
        self.estado_var = tk.StringVar(value="⏳ En espera…")
        tk.Label(self.root, textvariable=self.estado_var, bg=NORD["bg_dark"], fg=NORD["fg_dim"], font=("Helvetica", 9)).grid(row=3, column=0, columnspan=3, **pad)

        # --- Botón iniciar ---
        self.btn = tk.Button(self.root, 
                            text="🚀 Iniciar descarga", 
                            command=self._iniciar, 
                            width=20,
                            bg=NORD["green"],
                            fg=NORD["bg_dark"],
                            activebackground="#8FAC7A",  # Verde más oscuro
                            activeforeground=NORD["bg_dark"],
                            relief="raised",
                            borderwidth=2,
                            cursor="hand2",
                            font=("Helvetica", 10, "bold"))
        self.btn.grid(row=4, column=0, columnspan=3, pady=12)

    def _elegir_csv(self):
        ruta = filedialog.askopenfilename(filetypes=[("CSV", "*.csv"), ("Todos", "*.*")])
        if ruta:
            self.csv_var.set(ruta)

    def _elegir_dest(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.dest_var.set(carpeta)

    def _iniciar(self):
        csv_path = self.csv_var.get()
        dest_path = self.dest_var.get()

        if not os.path.exists(csv_path):
            messagebox.showerror("Error", f"No se encontró el archivo:\n{csv_path}")
            return

        df = pd.read_csv(csv_path)
        if "img_link" not in df.columns:
            messagebox.showerror("Error", "El CSV debe tener una columna llamada 'img_link'.")
            return

        os.makedirs(dest_path, exist_ok=True)
        self.btn.config(state="disabled", bg=NORD["border"], fg=NORD["fg_dim"])

        threading.Thread(target=self._descargar, args=(df, csv_path, dest_path), daemon=True).start()

    def _descargar(self, df, csv_path, dest_path):
        total = len(df)
        self.progreso["maximum"] = total
        paths, img_ids = [], []
        ref = 100000

        for i, link in enumerate(df["img_link"], start=1):
            img_id = "A" + str(i + ref)[1:]
            img_path = os.path.join(dest_path, img_id + ".jpg")
            self._estado(f"⬇️ Descargando {i}/{total}: {img_id}")

            try:
                res = requests.get(link, timeout=10)
                if res.status_code == 200:
                    with open(img_path, "wb") as f:
                        f.write(res.content)
                else:
                    self._estado(f"⚠️ Error {res.status_code} en imagen {i}/{total}")
            except Exception as e:
                self._estado(f"❌ Error de conexión: {e}")

            paths.append(img_path)
            img_ids.append(img_id)
            self.progreso["value"] = i
            self.root.update_idletasks()

        df["img_id"] = img_ids
        df["img_path"] = paths
        df.to_csv(csv_path, index=False)

        self._estado(f"✅ ¡Listo! {total} imágenes descargadas.")
        self.btn.config(state="normal", bg=NORD["green"], fg=NORD["bg_dark"])
        messagebox.showinfo("Listo", f"Se descargaron {total} imágenes en '{dest_path}'.")

    def _estado(self, msg):
        self.estado_var.set(msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = Descargador(root)
    root.mainloop()
