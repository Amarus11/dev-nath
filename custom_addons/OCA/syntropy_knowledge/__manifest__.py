# Copyright 2026 Syntropy
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Syntropy Knowledge Base",
    "version": "18.0.1.0.0",
    "category": "Knowledge Management",
    "summary": "Base de conocimiento dinámica e intuitiva para tu organización",
    "description": """
Syntropy Knowledge Base
========================
Módulo de gestión del conocimiento organizacional con:
- Artículos con editor HTML enriquecido y versionado
- Categorías jerárquicas para organización flexible
- Etiquetas (tags) para clasificación transversal
- Sistema de favoritos personales
- Vistas Kanban, Lista y Formulario intuitivas
- Control de acceso por roles (Lector / Editor / Administrador)
- Integración con chatter para colaboración
- Dashboard con métricas de uso
- Búsqueda avanzada por contenido, categoría, etiqueta y autor
    """,
    "author": "Syntropy",
    "website": "https://github.com/syntropy",
    "license": "LGPL-3",
    "depends": [
        "base",
        "mail",
        "web_editor",
    ],
    "data": [
        # Security
        "security/knowledge_security.xml",
        "security/ir.model.access.csv",
        # Data
        "data/knowledge_data.xml",
        # Views
        "views/knowledge_category_views.xml",
        "views/knowledge_tag_views.xml",
        "views/knowledge_article_views.xml",
        "views/knowledge_favorite_views.xml",
        # Menus (last, after all actions are defined)
        "views/knowledge_menus.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "syntropy_knowledge/static/src/scss/knowledge.scss",
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
}
