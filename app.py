from flask import Flask, request, redirect
import datetime as dt

app = Flask(__name__)

# --- TES VARIABLES (gardées telles quelles) ---
id_tache = 1
liste_tache = []

# --- TES FONCTIONS (gardées telles quelles) ---

def add_tache_web(description, echeance_str):
    """Version web de ta fonction add_tache"""
    global id_tache
    
    try:
        # Conversion de la date (même format que dans ton code)
        echeance = dt.datetime.strptime(echeance_str, "%d/%m/%Y/%H")
        
        # Création de la tâche (identique à ton code)
        tache = {
            "id": id_tache,
            "description": description,
            "echeance": echeance,
            "statut": "en cours",
            "date_creation": dt.datetime.now()
        }
        
        liste_tache.append(tache)
        id_tache += 1
        return True, f"Tâche #{tache['id']} ajoutée avec succès !"
        
    except ValueError:
        return False, "Format de date incorrect ! Utilisez jj/mm/aaaa/HH"

def del_tache_web(tache_id):
    """Version web de ta fonction del_tache"""
    global liste_tache
    liste_tache = [t for t in liste_tache if t['id'] != tache_id]
    return f"Tâche #{tache_id} supprimée !"

def done_tache_web(tache_id):
    """Version web de ta fonction done_tache"""
    for t in liste_tache:
        if t['id'] == tache_id:
            if t['statut'] == "terminée":
                return "Cette tâche est déjà terminée"
            else:
                t['statut'] = "terminée"
                return f"Tâche #{tache_id} terminée ! Bravo champion !"
    return "Cette tâche n'existe pas"

# --- FONCTION POUR GÉNÉRER LE HTML ---

def generer_html(message=""):
    """Génère tout le HTML directement dans Python"""
    
    # HTML des tâches
    html_taches = ""
    if liste_tache:
        for tache in liste_tache:
            # Calculer si l'échéance est dépassée
            maintenant = dt.datetime.now()
            echeance_depassee = tache['echeance'] < maintenant
            
            html_taches += f"""
            <div class="tache {'terminee' if tache['statut'] == 'terminée' else ''} {'urgence' if echeance_depassee and tache['statut'] != 'terminée' else ''}">
                <div class="tache-info">
                    <h3>📝 {tache['description']}</h3>
                    <div class="tache-details">
                        <span class="badge">🆔 ID: {tache['id']}</span>
                        <span class="badge">📅 Créée: {tache['date_creation'].strftime('%d/%m/%Y %H:%M')}</span>
                        <span class="badge {'urgence' if echeance_depassee and tache['statut'] != 'terminée' else ''}">
                            ⏰ Échéance: {tache['echeance'].strftime('%d/%m/%Y à %H:%M')}
                            {'⌛ LA DATE EST PASSÉE!, il faut revoir ta date bro' if echeance_depassee and tache['statut'] != 'terminée' else ''}
                        </span>
                        <span class="badge {'statut-termine' if tache['statut'] == 'terminée' else 'statut-en-cours'}">
                            {tache['statut'].upper()}
                        </span>
                    </div>
                </div>
                <div class="tache-actions">
                    {'' if tache['statut'] == 'terminée' else f'<a href="/done/{tache["id"]}" class="btn btn-termine">✅ Terminer</a>'}
                    <a href="/delete/{tache["id"]}" class="btn btn-supprimer" onclick="return confirm(\'Supprimer cette tâche ?\')">🗑️ Supprimer</a>
                </div>
            </div>
            """
    else:
        html_taches = """
        <div class="vide">
            <div style="font-size: 72px; margin-bottom: 20px;">📭</div>
            <h3>Aucune tâche pour le moment</h3>
            <p>Commence par ajouter ta première tâche stp bro !</p>
        </div>
        """
    
    # Message de notification
    html_message = ""
    if message:
        html_message = f"""
        <div class="notification">
            {message}
            <button onclick="this.parentElement.style.display='none'">×</button>
        </div>
        """
    
    # HTML COMPLET
    html = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🏆 To-Do List de JB La Légende</title>
        <style>
            /* === RESET === */
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Arial', sans-serif;
            }}
            
            /* === BACKGROUND === */
            body {{
                background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
                min-height: 100vh;
                padding: 20px;
                color: white;
            }}
            
            /* === CONTAINER === */
            .container {{
                max-width: 1000px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 25px;
                padding: 30px;
                backdrop-filter: blur(10px);
                border: 2px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            }}
            
            /* === HEADER === */
            .header {{
                text-align: center;
                margin-bottom: 40px;
                padding-bottom: 20px;
                border-bottom: 3px solid rgba(255, 215, 0, 0.3);
            }}
            
            .header h1 {{
                font-size: 3rem;
                background: linear-gradient(45deg, #FFD700, #FFA500);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            }}
            
            .header p {{
                color: #aaa;
                font-size: 1.2rem;
                margin-top: 10px;
            }}
            
            /* === NOTIFICATION === */
            .notification {{
                background: linear-gradient(90deg, #4CAF50, #45a049);
                color: white;
                padding: 15px 20px;
                border-radius: 10px;
                margin-bottom: 30px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                animation: slideIn 0.5s ease-out;
            }}
            
            .notification button {{
                background: none;
                border: none;
                color: white;
                font-size: 24px;
                cursor: pointer;
                padding: 0 10px;
            }}
            
            /* === MENU STYLE CONSOLE MODERNE === */
.menu-console {{
    background: linear-gradient(135deg, rgba(10,10,10,0.95), rgba(30,30,30,0.95));
    padding: 30px;
    border-radius: 18px;
    margin-bottom: 40px;
    border-left: 5px solid #FFD700;
    box-shadow: 0 10px 30px rgba(0,0,0,0.6);
}}

/* Titre du menu */
.menu-title {{
    color: #ffffff;
    font-size: 1.9rem;
    margin-bottom: 22px;
    text-align: center;
    letter-spacing: 2px;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
}}

/* Texte console */
.console-text {{
    font-family: 'Courier New', monospace;
    background: radial-gradient(circle at top, #111, #000);
    padding: 22px;
    border-radius: 12px;
    margin: 18px 0;
    color: #ffffff;
    border: 1px solid #444;
    box-shadow: inset 0 0 10px rgba(255, 255, 255, 0.08);
    line-height: 1.6;
    transition: 0.3s ease-in-out;
}}

/* Effet au survol */
.console-text:hover {{
    box-shadow: inset 0 0 15px rgba(255, 215, 0, 0.3);
    transform: scale(1.01);
}}
.instruction-list {{
    list-style-type: none;
    padding-left: 0;
}}
.instruction-list li {{
    margin-bottom: 10px;
    font-size: 1.1rem;
}}

            
            /* === FORMULAIRE === */
            .form-container {{
                background: rgba(255, 255, 255, 0.08);
                padding: 30px;
                border-radius: 20px;
                margin-bottom: 40px;
                border: 2px dashed rgba(255, 255, 255, 0.2);
            }}
            
            .form-group {{
                margin-bottom: 25px;
            }}
            
            label {{
                display: block;
                margin-bottom: 10px;
                color: #FFD700;
                font-weight: bold;
                font-size: 1.1rem;
            }}
            
            input {{
                width: 100%;
                padding: 15px;
                border: 2px solid #444;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.1);
                color: white;
                font-size: 16px;
                transition: all 0.3s;
            }}
            
            input:focus {{
                outline: none;
                border-color: #FF416C;
                box-shadow: 0 0 15px rgba(255, 65, 108, 0.3);
                transform: translateY(-2px);
            }}
            
            .btn-submit {{
                background: linear-gradient(45deg, #FF416C, #FF4B2B);
                color: white;
                border: none;
                padding: 18px 35px;
                border-radius: 12px;
                font-size: 1.2rem;
                font-weight: bold;
                cursor: pointer;
                width: 100%;
                transition: all 0.3s;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            
            .btn-submit:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(255, 65, 108, 0.4);
            }}
            
            /* === LISTE DES TÂCHES === */
            .tasks-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid rgba(255, 255, 255, 0.2);
            }}
            
            .task-count {{
                background: linear-gradient(45deg, #FF416C, #FF4B2B);
                padding: 12px 24px;
                border-radius: 25px;
                font-weight: bold;
                font-size: 1.2rem;
                box-shadow: 0 5px 15px rgba(255, 65, 108, 0.3);
            }}
            
            /* === TÂCHE INDIVIDUELLE === */
            .tache {{
                background: rgba(255, 255, 255, 0.05);
                border-left: 8px solid #4169E1;
                padding: 25px;
                margin-bottom: 20px;
                border-radius: 15px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                transition: all 0.3s;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            }}
            
            .tache:hover {{
                transform: translateY(-5px);
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
            }}
            
            .tache.terminee {{
                border-left-color: #4CAF50;
                background: rgba(76, 175, 80, 0.1);
                opacity: 0.8;
            }}
            
            .tache.urgence {{
                border-left-color: #FF5722;
                background: rgba(255, 87, 34, 0.1);
                animation: pulse 2s infinite;
            }}
            
            .tache-info h3 {{
                font-size: 1.4rem;
                margin-bottom: 15px;
                color: white;
            }}
            
            .tache-details {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }}
            
            .badge {{
                background: rgba(255, 255, 255, 0.1);
                padding: 8px 15px;
                border-radius: 20px;
                font-size: 0.9rem;
            }}
            
            .badge.urgence {{
                background: rgba(255, 87, 34, 0.3);
                color: #FF5722;
                font-weight: bold;
            }}
            
            .badge.statut-termine {{
                background: rgba(76, 175, 80, 0.3);
                color: #4CAF50;
            }}
            
            .badge.statut-en-cours {{
                background: rgba(33, 150, 243, 0.3);
                color: #2196F3;
            }}
            
            /* === BOUTONS D'ACTION === */
            .tache-actions {{
                display: flex;
                gap: 15px;
            }}
            
            .btn {{
                padding: 12px 25px;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                transition: all 0.3s;
                font-size: 1rem;
            }}
            
            .btn-termine {{
                background: linear-gradient(45deg, #4CAF50, #45a049);
                color: white;
            }}
            
            .btn-termine:hover {{
                transform: translateY(-3px);
                box-shadow: 0 8px 20px rgba(76, 175, 80, 0.3);
            }}
            
            .btn-supprimer {{
                background: linear-gradient(45deg, #f44336, #d32f2f);
                color: white;
            }}
            
            .btn-supprimer:hover {{
                transform: translateY(-3px);
                box-shadow: 0 8px 20px rgba(244, 67, 54, 0.3);
            }}
            
            /* === ÉTAT VIDE === */
            .vide {{
                text-align: center;
                padding: 60px 30px;
                color: #aaa;
            }}
            
            .vide div {{
                font-size: 4rem;
                margin-bottom: 20px;
                opacity: 0.5;
            }}
            
            /* === FOOTER === */
            .footer {{
                text-align: center;
                margin-top: 50px;
                padding-top: 30px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                color: #888;
            }}
            
            /* === ANIMATIONS === */
            @keyframes slideIn {{
                from {{ transform: translateY(-20px); opacity: 0; }}
                to {{ transform: translateY(0); opacity: 1; }}
            }}
            
            @keyframes pulse {{
                0% {{ box-shadow: 0 0 0 0 rgba(255, 87, 34, 0.7); }}
                70% {{ box-shadow: 0 0 0 10px rgba(255, 87, 34, 0); }}
                100% {{ box-shadow: 0 0 0 0 rgba(255, 87, 34, 0); }}
            }}
            
            /* === RESPONSIVE === */
            @media (max-width: 768px) {{
                .container {{
                    padding: 20px;
                }}
                
                .header h1 {{
                    font-size: 2.2rem;
                }}
                
                .tache {{
                    flex-direction: column;
                    text-align: center;
                }}
                
                .tache-details {{
                    justify-content: center;
                    margin-bottom: 15px;
                }}
                
                .tache-actions {{
                    width: 100%;
                    justify-content: center;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- HEADER -->
            <div class="header">
                <h1>🏆 TO-DO LIST DE JB LA LÉGENDE 🏆</h1>
                <p>"la légende est la pour vous aider à gérer vos tâches "</p>
            </div>
            
            <!-- MESSAGE -->
            {html_message}
            
            <!-- MENU COMME TA CONSOLE -->
            <div class="menu-console">
                <div class="menu-title">💻 MENU PRINCIPAL</div>
                <div class="console-text">

                    Bonjour monsieur/madame.<br>
                    Nous vous souhaitons la bienvenue dans to-do list de JB LA LÉGENDE. AKWABA à vous <br>
                    Voici comment utiliser cette application légendaire :<br>

                    <ul class="instruction-list">
                <li>📝 <strong>Utilisez le formulaire</strong> pour AJOUTER une tâche</li>
                <li>✅ <strong>Cliquez</strong> pour TERMINER une tâche</li>
                <li>🗑️ <strong>Cliquez</strong> pour SUPPRIMER une tâche</li>
                <li>📋 <strong>La liste des tâches</strong> s’affiche automatiquement ci-dessous</li>
</ul> <br>
                </div>
            </div>
            
            <!-- FORMULAIRE D'AJOUT -->
            <div class="form-container">
                <h2 style="color: #FFD700; margin-bottom: 25px; text-align: center;">
                    <i class="fas fa-plus-circle"></i> AJOUTER UNE TÂCHE
                </h2>
                
                <form action="/add" method="POST">
                    <div class="form-group">
                        <label for="description">📝 Description :</label>
                        <input type="text" id="description" name="description" 
                               placeholder="Ex: chercher les enfants à l'école, Apprendre Python..." 
                               required>
                    </div>
                    
                    <div class="form-group">
                        <label for="echeance">📅 Date d'échéance :</label>
                        <input type="text" id="echeance" name="echeance" 
                               placeholder="Format: jj/mm/aaaa/HH (ex: 25/12/2024/14)" 
                               required>
                        <small style="color: #aaa; display: block; margin-top: 8px;">
                            ⓘ Format exact: Jour/Mois/Année/Heure (24h)
                        </small>
                    </div>
                    
                    <button type="submit" class="btn-submit">
                        🚀 CLIQUER POUR AJOUTER UNE TÂCHE 
                    </button>
                </form>
            </div>
            
            <!-- LISTE DES TÂCHES -->
            <div class="tasks-header">
                <h2 style="color: white;">📋 Liste de Suivi des Tâches</h2>
                <div class="task-count">
                    {len(liste_tache)} TÂCHE{'S' if len(liste_tache) != 1 else ''}
                </div>
            </div>
            
            <div class="tasks-list">
                {html_taches}
            </div>
            
            <!-- FOOTER PROFESSIONNEL -->
<div class="footer">
    <div class="footer-content">
        
       <div class="footer-left">
           <img src="/static/jb.jpeg" alt="Jean-Baptiste Koffi" class="footer-avatar" style="width: 300px; height: 300px; border-radius: 80%;">
</div>


        <div class="footer-right">
            <p class="footer-name">
                Développé avec passion par <strong>Jean-Baptiste Koffi</strong>
            </p>
            <p class="footer-tech">
                💻 Python & Flask
            </p>
            <p class="footer-date">
    📅 {dt.datetime.now().strftime('%d/%m/%Y %H:%M')}
</p>
        </div>

    </div>
</div>

        
        <script>
            // Confirmation pour suppression
            document.querySelectorAll('.btn-supprimer').forEach(button => {{
                button.addEventListener('click', function(e) {{
                    if (!confirm('Êtes-vous sûr de vouloir supprimer cette tâche légendaire ?')) {{
                        e.preventDefault();
                    }}
                }});
            }});
            
            // Auto-suppression des notifications après 5 secondes
            setTimeout(() => {{
                const notifications = document.querySelectorAll('.notification');
                notifications.forEach(notification => {{
                    notification.style.display = 'none';
                }});
            }}, 5000);
            
            // Focus sur le premier champ
            document.getElementById('description').focus();
            
            console.log('🏆 To-Do List de JB La Légende - Prête à gérer tes tâches !');
        </script>
    </body>
    </html>
    """
    
    return html

# --- VARIABLE POUR LES MESSAGES ---
last_message = ""

# --- ROUTES ---

@app.route('/')
def index():
    return generer_html(last_message)

@app.route('/add', methods=['POST'])
def add_tache_route():
    global last_message
    description = request.form.get('description')
    echeance_str = request.form.get('echeance')
    
    if description and echeance_str:
        succes, message = add_tache_web(description, echeance_str)
        last_message = message
    else:
        last_message = "❌ Veuillez remplir tous les champs !"
    
    return redirect('/')

@app.route('/delete/<int:tache_id>')
def delete_tache_route(tache_id):
    global last_message
    last_message = del_tache_web(tache_id)
    return redirect('/')

@app.route('/done/<int:tache_id>')
def done_tache_route(tache_id):
    global last_message
    last_message = done_tache_web(tache_id)
    return redirect('/')

# --- LANCEMENT ---
if __name__ == '__main__':
    
    app.run(debug=True, port=5000)