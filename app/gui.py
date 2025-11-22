from pathlib import Path
from tkinter import Tk, Frame, Label, Entry, Button, filedialog, messagebox
from tkinter import ttk

from .config_loader import load_positions, DEFAULT_CONFIG_PATH
from .models import BudgetData, ClientData, PlanData, VehicleData
from .paths import resource_path
from .pdf_generator import generate_budget_pdf


class BudgetApp:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("Generador de Presupuestos PDF")
        self.config_path = DEFAULT_CONFIG_PATH
        self.template_path = resource_path("resources/plantilla_base.pdf")
        self.positions = load_positions(self.config_path)

        self.entries = {}
        container = Frame(root, padx=10, pady=10)
        container.pack(fill="both", expand=True)

        self._build_section(container, "Cliente", [
            ("Nombre", "cliente_nombre"),
            ("Documento", "cliente_documento"),
            ("Teléfono", "cliente_telefono"),
            ("Correo", "cliente_correo"),
            ("Dirección", "cliente_direccion"),
        ])

        self._build_section(container, "Plan", [
            ("Nombre del plan", "plan_plan_nombre"),
            ("Cuota", "plan_plan_cuota"),
            ("Condiciones", "plan_plan_condiciones"),
        ])

        self._build_section(container, "Vehículo", [
            ("Modelo", "vehiculo_modelo"),
            ("Año", "vehiculo_anio"),
            ("Precio", "vehiculo_precio"),
            ("Color", "vehiculo_color"),
            ("Versión", "vehiculo_version"),
        ])

        btn_frame = Frame(container, pady=10)
        btn_frame.pack(fill="x")

        Button(btn_frame, text="Seleccionar plantilla PDF", command=self.select_template).pack(side="left", padx=5)
        Button(btn_frame, text="Seleccionar config JSON", command=self.select_config).pack(side="left", padx=5)
        Button(btn_frame, text="Generar PDF", command=self.generate).pack(side="right", padx=5)

    def _build_section(self, parent: Frame, title: str, fields: list[tuple[str, str]]):
        frame = ttk.LabelFrame(parent, text=title)
        frame.pack(fill="x", pady=5)
        for idx, (label_text, key) in enumerate(fields):
            Label(frame, text=label_text).grid(row=idx, column=0, sticky="w", padx=5, pady=2)
            entry = Entry(frame, width=40)
            entry.grid(row=idx, column=1, padx=5, pady=2)
            self.entries[key] = entry

    def select_template(self):
        path = filedialog.askopenfilename(
            title="Seleccionar plantilla PDF",
            filetypes=[("PDF", "*.pdf")],
            initialdir=str(Path(self.template_path).parent),
        )
        if path:
            self.template_path = Path(path)
            messagebox.showinfo("Plantilla", f"Plantilla seleccionada:\n{self.template_path}")

    def select_config(self):
        path = filedialog.askopenfilename(
            title="Seleccionar configuración JSON",
            filetypes=[("JSON", "*.json")],
            initialdir=str(Path(self.config_path).parent),
        )
        if path:
            self.config_path = Path(path)
            try:
                self.positions = load_positions(self.config_path)
            except Exception as exc:  # pylint: disable=broad-except
                messagebox.showerror("Error", f"No se pudo cargar la configuración: {exc}")
                return
            messagebox.showinfo("Configuración", f"Configuración cargada desde:\n{self.config_path}")

    def generate(self):
        try:
            budget = self._collect_data()
            output_path = Path(f"presupuesto_{budget.cliente.nombre or 'cliente'}.pdf")
            generate_budget_pdf(budget, self.positions, self.template_path, output_path)
            messagebox.showinfo("Éxito", f"PDF generado en:\n{output_path.resolve()}")
        except Exception as exc:  # pylint: disable=broad-except
            messagebox.showerror("Error", f"No se pudo generar el PDF: {exc}")

    def _collect_data(self) -> BudgetData:
        def get(key: str) -> str:
            return self.entries[key].get()

        cliente = ClientData(
            nombre=get("cliente_nombre"),
            documento=get("cliente_documento"),
            telefono=get("cliente_telefono"),
            correo=get("cliente_correo"),
            direccion=get("cliente_direccion"),
        )
        plan = PlanData(
            plan_nombre=get("plan_plan_nombre"),
            plan_cuota=get("plan_plan_cuota"),
            plan_condiciones=get("plan_plan_condiciones"),
        )
        vehiculo = VehicleData(
            modelo=get("vehiculo_modelo"),
            anio=get("vehiculo_anio"),
            precio=get("vehiculo_precio"),
            color=get("vehiculo_color"),
            version=get("vehiculo_version"),
        )
        return BudgetData(cliente=cliente, plan=plan, vehiculo=vehiculo)


def run_app():
    root = Tk()
    BudgetApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()
