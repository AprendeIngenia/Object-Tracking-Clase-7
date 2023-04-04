# Importamos las librerias
import dlib
import cv2
import get_points

# Creamos nuestra captura de video
cap = cv2.VideoCapture(0)
print('Pulsa P para pausar el video y empezar el seguimiento')

def tracker(img, puntos):
    # Coordenadas iniciales del objeto a rastrear.
    # Crear el objeto de seguimiento
    tracker = dlib.correlation_tracker()
    # Proporcionar al rastreador la posición inicial del objeto.
    tracker.start_track(img, dlib.rectangle(*points[0]))
    while True:
        # Se lee la imagen desde el aparato o archivo
        ret, img = cap.read()
        if not ret:
            print("No se ejecuto la captura :(")
            exit()
        # Actualizacion del seguimiento
        tracker.update(img)
        # Se obtiene la posición del objeto, se dibujar un
        # cuadro de límite alrededor de él y lo muestra.
        rect = tracker.get_position()
        pt1 = (int(rect.left()), int(rect.top()))
        pt2 = (int(rect.right()), int(rect.bottom()))
        cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)
        print("Objecto tracked en [{}, {}] \r".format(pt1, pt2), )
        loc = (int(rect.left()), int(rect.top() - 20))
        txt = "Objecto tracked en [{}, {}]".format(pt1, pt2)
        cv2.putText(img, txt, loc, cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1)
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", img)
        # Continua hasta que se pulsa Escape
        if cv2.waitKey(1) == 27:
            break

# Empezamos nuestro while
while True:
    # Leemos los frames
    ret, frame = cap.read()

    # Leemos el teclado
    t = cv2.waitKey(1)

    # Si no hay captura
    if not ret:
        print('No se pudo capturar la camara')
        exit()

    # Si oprimimos P cerramos
    if (t == ord('p')):
        # Las coordenadas de los objetos a rastrear
        # se almacenarán en una lista llamada `puntos`
        points = get_points.run(frame)
        if not points:
            print("ERROR: No objeto para seguimiento.")
            exit()
        if points:
            tracker(img = frame, puntos = points)
        break

    # Mostramos los frame
    cv2.imshow("IMAGEN", frame)



# Cerramos la ventana
cv2.destroyAllWindows()

