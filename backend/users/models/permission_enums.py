from enum import Enum

class PermissionCode(Enum):
    # Usuarios
    USER_VIEW = "user_view"
    USER_EDIT = "user_edit"
    USER_DELETE = "user_delete"
    USER_CREATE = "user_create"

    # Planes
    PLAN_VIEW = "plan_view"
    PLAN_CREATE = "plan_create"
    PLAN_EDIT = "plan_edit"
    PLAN_DELETE = "plan_delete"

    # Perfil fitness
    FITNESS_PROFILE_VIEW = "fitness_profile_view"
    FITNESS_PROFILE_EDIT = "fitness_profile_edit"
    FITNESS_PROFILE_DELETE = "fitness_profile_delete"

    # Conversación
    CONVERSATION_VIEW = "conversation_view"
    CONVERSATION_CREATE = "conversation_create"
    CONVERSATION_RESPOND = "conversation_respond"
    CONVERSATION_RESET = "conversation_reset"

    # Preguntas
    QUESTION_VIEW = "question_view"
    QUESTION_CREATE = "question_create"
    QUESTION_EDIT = "question_edit"
    QUESTION_DELETE = "question_delete"

    # Feedback
    FEEDBACK_VIEW = "feedback_view"
    FEEDBACK_CREATE = "feedback_create"
    FEEDBACK_EDIT = "feedback_edit"
    FEEDBACK_DELETE = "feedback_delete"

    # Notificaciones
    NOTIFICATION_VIEW = "notification_view"
    NOTIFICATION_CREATE = "notification_create"
    NOTIFICATION_EDIT = "notification_edit"
    NOTIFICATION_DELETE = "notification_delete"

    # Admin
    ADMIN_PANEL_ACCESS = "admin_panel_access" 