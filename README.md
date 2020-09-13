# LightPi
Control de pantalla HDMI con sensor LDR en Raspberry Pi

Programa que permite controlar el encedido y apagado de pantalla HDMI conectada a una Raspberri Pi mediante un sensor de luz LDR, en este caso se encuentra conectado al pin 7

Dependiendo de las condiciones de iluminacion puede ajustarse el valor de i

# Conexion

https://pi.lbbcdn.com/wp-content/uploads/2016/01/Light-Sensor-Circuit.jpg


## Instalar como un servicio


Ahora vamos a definir el servicio para ejecutar este script:

```Shell
cd /lib/systemd/system/
sudo nano lightpi.service
```

La definición del servicio debe estar en la carpeta /lib/systemd/system. Nuestro servicio se llamará "lightpi.service":

```text
[Unit]
Description=LightPi
After=multi-user.target

[Service]
Type=simple
ExecStart=sudo python /home/pi/LightPi.py
Restart=on-abort

[Install]
WantedBy=multi-user.target
```

Aquí estamos creando un servicio muy simple que ejecuta nuestro script y si de alguna manera se cancela, se reiniciará automáticamente. Puede consultar más sobre las opciones del servicio en la siguiente wiki: https://wiki.archlinux.org/index.php/systemd.


Ahora que tenemos nuestro servicio necesitamos activarlo:

```Shell
sudo chmod 644 /lib/systemd/system/lightpi.service
chmod +x /home/pi/LightPi.py
sudo systemctl daemon-reload
sudo systemctl enable lightpi.service
sudo systemctl start lightpi.service
```

### Check status
`sudo systemctl status lightpi.service`

