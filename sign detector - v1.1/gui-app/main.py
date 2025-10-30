def iniciar_aplicacion():
    import tkinter as tk
    from tkinter import filedialog, messagebox
    from PIL import Image, ImageTk
    import onnxruntime
    import numpy as np
    from torchvision import transforms
    import cv2
    import os
    import sys

   
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    model_path = resource_path("onnx_model/stacked_model_mobilenet_resnet.onnx")
    session = onnxruntime.InferenceSession(model_path)

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

    class_names = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
        'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
        'Y', 'Z', 'borrar', 'nada', 'espacio'
    ]

    selected_image_path = None

    # -----------------------
    def preprocess_image(image_path):
        img = Image.open(image_path).convert('RGB')
        img_t = transform(img)
        img_np = img_t.numpy()
        return img_np[np.newaxis, ...]

    def show_image(path):
        img = Image.open(path).convert('RGB')
        img.thumbnail((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk

    def select_image():
        nonlocal selected_image_path
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.jpg *.png *.jpeg")]
        )
        if not file_path:
            return
        selected_image_path = file_path
        show_image(file_path)

    def predict_selected_image():
        if not selected_image_path:
            messagebox.showwarning("Advertencia", "Primero selecciona una imagen.")
            return
        try:
            input_image = preprocess_image(selected_image_path)
            input_name = session.get_inputs()[0].name
            outputs = session.run(None, {input_name: input_image})

            probabilidades = outputs[0][0]
            indice_predicho = np.argmax(probabilidades)
            probabilidades_softmax = np.exp(probabilidades) / np.sum(np.exp(probabilidades))
            confianza = probabilidades_softmax[indice_predicho] * 100
            letra_predicha = class_names[indice_predicho]

            result = f"Letra detectada: {letra_predicha}\nConfianza: {confianza:.2f}%"
            precision_general = 91.73
            result += f"\nPrecisión general del modelo: {precision_general:.2f}%"

            messagebox.showinfo("Resultado", result)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar la imagen.\n\n{e}")

    def capture_from_camera():
        nonlocal selected_image_path

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "No se pudo acceder a la cámara.")
            return

        cam_window = tk.Toplevel()
        cam_window.title("Cámara activa")
        cam_window.geometry("400x300")

        lmain = tk.Label(cam_window)
        lmain.pack()

        def show_frame():
            ret, frame = cap.read()
            if ret:
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img.resize((350, 250)))
                lmain.imgtk = imgtk
                lmain.configure(image=imgtk)
                lmain.after(10, show_frame)

        def capture_and_close():
            ret, frame = cap.read()
            if ret:
                temp_image_path = "captura_temp.jpg"
                cv2.imwrite(temp_image_path, frame)
                cap.release()
                cam_window.destroy()
                nonlocal selected_image_path
                selected_image_path = temp_image_path
                show_image(selected_image_path)
                predict_selected_image()
                # 🔥 Eliminar la imagen temporal
                try:
                    os.remove(temp_image_path)
                except Exception as e:
                    print(f"Advertencia: No se pudo eliminar la imagen temporal: {e}")

        btn_capturar = tk.Button(cam_window, text="Capturar", command=capture_and_close,
                                 bg="#ff9800", fg="white", font=("Arial", 12))
        btn_capturar.pack(pady=10)

        show_frame()

    # -----------------------
    # Interfaz gráfica
    root = tk.Tk()
    root.title("Detector de Letras con ONNX")
    root.geometry("350x450")
    root.configure(bg="#1e1e2f")

    title_label = tk.Label(root, text="Detector de Lenguaje de Señas", font=("Arial", 16, "bold"),
                           fg="#00e5ff", bg="#1e1e2f")
    title_label.pack(pady=15)

    image_label = tk.Label(root, bg="#1e1e2f")
    image_label.pack(pady=10)

    btn_select = tk.Button(root, text="Seleccionar Imagen", command=select_image,
                           bg="#2196f3", fg="white", font=("Arial", 12))
    btn_select.pack(pady=5)

    btn_camera = tk.Button(root, text="Abrir Cámara", command=capture_from_camera,
                           bg="#ff9800", fg="white", font=("Arial", 12))
    btn_camera.pack(pady=5)

    btn_verify = tk.Button(root, text="Verificar Imagen", command=predict_selected_image,
                           bg="#4caf50", fg="white", font=("Arial", 12))
    btn_verify.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()
