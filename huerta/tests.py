from datetime import date, timedelta

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Agricultor, Cultivo


class HuertaAPITests(APITestCase):
    def setUp(self):
        self.marta = Agricultor.objects.create(nombre="Marta Ríos", parcela="Parcela 1")

    def datos_cultivo(self, **extra):
        datos = {
            "nombre": "Tomate",
            "tipo": "hortaliza",
            "estado": "sembrado",
            "fecha_siembra": str(date.today() - timedelta(days=10)),
            "ofrece": "cosecha",
            "cantidad": 3,
            "unidad": "kg",
            "agricultor": self.marta.id,
        }
        datos.update(extra)
        return datos

    # --- Agricultor ---
    def test_crud_agricultor(self):
        r = self.client.post(
            "/api/agricultores/", {"nombre": "Luisa", "parcela": "Parcela 2"}, format="json"
        )
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        pk = r.data["id"]

        r = self.client.get("/api/agricultores/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 2)

        r = self.client.patch(f"/api/agricultores/{pk}/", {"parcela": "Parcela 9"}, format="json")
        self.assertEqual(r.data["parcela"], "Parcela 9")

        r = self.client.delete(f"/api/agricultores/{pk}/")
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

    # --- Cultivo ---
    def test_crud_cultivo_con_fk(self):
        r = self.client.post("/api/cultivos/", self.datos_cultivo(), format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED, r.data)
        self.assertEqual(r.data["agricultor_nombre"], "Marta Ríos")
        pk = r.data["id"]

        r = self.client.patch(f"/api/cultivos/{pk}/", {"estado": "listo"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["estado_display"], "Listo para cosechar")

        r = self.client.delete(f"/api/cultivos/{pk}/")
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cultivo.objects.count(), 0)

    def test_total_cultivos_en_agricultor(self):
        self.client.post("/api/cultivos/", self.datos_cultivo(), format="json")
        r = self.client.get("/api/agricultores/")
        self.assertEqual(r.data[0]["total_cultivos"], 1)

    def test_rechaza_oferta_sin_cantidad(self):
        r = self.client.post("/api/cultivos/", self.datos_cultivo(cantidad=0), format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("cantidad", r.data)

    def test_rechaza_fecha_futura(self):
        futura = str(date.today() + timedelta(days=5))
        r = self.client.post("/api/cultivos/", self.datos_cultivo(fecha_siembra=futura), format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("fecha_siembra", r.data)

    def test_rechaza_agricultor_inexistente(self):
        r = self.client.post("/api/cultivos/", self.datos_cultivo(agricultor=9999), format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filtros(self):
        otro = Agricultor.objects.create(nombre="Efraín", parcela="Parcela 2")
        self.client.post("/api/cultivos/", self.datos_cultivo(), format="json")
        self.client.post(
            "/api/cultivos/",
            self.datos_cultivo(nombre="Lulo", ofrece="semillas", unidad="sobres", agricultor=otro.id),
            format="json",
        )
        self.assertEqual(len(self.client.get(f"/api/cultivos/?agricultor={otro.id}").data), 1)
        self.assertEqual(len(self.client.get("/api/cultivos/?ofrece=cosecha").data), 1)
        self.assertEqual(len(self.client.get("/api/cultivos/").data), 2)

    def test_eliminar_agricultor_elimina_sus_cultivos(self):
        self.client.post("/api/cultivos/", self.datos_cultivo(), format="json")
        self.client.delete(f"/api/agricultores/{self.marta.id}/")
        self.assertEqual(Cultivo.objects.count(), 0)

    # --- CORS ---
    def test_cors_permite_origen_del_cliente(self):
        r = self.client.get("/api/cultivos/", HTTP_ORIGIN="http://localhost:5173")
        self.assertEqual(r["Access-Control-Allow-Origin"], "http://localhost:5173")
