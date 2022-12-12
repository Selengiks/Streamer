from aiogram.dispatcher.filters.state import State, StatesGroup


class FSM(StatesGroup):

    """Main state of the bot"""
    primary = State()

    """State for find_user method"""
    find_user = State()

    """Add user logic"""
    add_user_step_user = State()
    add_user_step_source = State()
    add_user_step_sub = State()
    add_user_step_teamlead = State()

    """Delete user logic"""
    del_user_step_user = State()

    """Add user sub logic"""
    add_sub_step_user = State()  #
    add_sub_step_source = State()  #
    add_sub_step_sub = State()  #

    """Add user campaign logic"""
    add_camp_step_user = State()
    add_camp_step_app = State()
    add_camp_step_sub = State()

    """Open organic logic"""
    open_org_step_user = State()  #
    open_org_step_app = State()  #

    """Close organic logic"""
    close_org_step_user = State()  #
    close_org_step_app = State()  #

    "Allow organic edit logic"
    allow_edit_org_step_user = State()  #
    allow_edit_org_step_app = State()  #

    """Add visibility for financier"""
    open_fin_visib_step_app = State()  #

    """Service state for some shit"""
    temp_state = State()
