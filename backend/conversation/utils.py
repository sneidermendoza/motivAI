from plans.models.plan import UserFitnessProfile

def extract_and_update_fitness_profile(usuario, plan, response):
    """
    Extrae información relevante de la respuesta y actualiza o crea el UserFitnessProfile asociado.
    """
    # Determinar el campo a actualizar según la pregunta
    question = response.question
    text = response.raw_text.strip()
    if not question or not text:
        return

    # Buscar o crear el perfil fitness para este usuario y plan
    profile, created = UserFitnessProfile.objects.get_or_create(usuario=usuario, plan=plan)

    # Lógica simple basada en el texto de la pregunta
    q_text = question.text.lower() if question else ''
    if 'motivación' in q_text or 'motiva' in q_text:
        profile.motivacion = text
    elif 'objetivo' in q_text:
        profile.objetivo = text
    elif 'edad' in q_text:
        try:
            profile.edad = int(text)
        except ValueError:
            pass
    elif 'sexo' in q_text:
        profile.sexo = text.lower()
    elif 'peso' in q_text:
        try:
            profile.peso = float(text.replace(',', '.'))
        except ValueError:
            pass
    elif 'altura' in q_text:
        try:
            profile.altura = float(text.replace(',', '.'))
        except ValueError:
            pass
    elif 'actividad' in q_text:
        profile.nivel_actividad = text
    elif 'restriccion' in q_text or 'restricción' in q_text:
        profile.restricciones = text
    else:
        # Guardar en 'otros' si no es un campo conocido
        otros = profile.otros or {}
        otros[q_text] = text
        profile.otros = otros

    profile.save() 