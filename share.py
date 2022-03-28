import smtplib
import webbrowser
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from plyer import notification
from utils import *


class App:
    def __init__(self, master):
        self.main_panel = master

        self.new_qr_codes = StringVar()
        self.star_label = None
        self.email_taskbar = None
        self.username_label_taskbar = None
        self.number_list_items_label = None
        self.clicked_user_drop = None
        self.clicked_user = None
        self.taskbar_frame = None
        self.current_page = None
        self.theme_value = None
        self.font_value_var = None
        self.upi_id_var = None
        self.phone_number_var = None
        self.email_password_var = None
        self.email_var = None
        self.name_var = None
        self.setting_window = None
        self.right_bottom_frame = None
        self.left_theme_frame = None
        self.left_profile_frame = None
        self.right_top_frame = None
        self.event_name_entry = None
        self.item = None
        self.list_of_items_frame = None
        self.money_var = None
        self.new_member_window = None
        self.new_entry_frame = None
        self.first_row_frame = None
        self.event = StringVar()
        self.list_of_members = []
        self.items = []
        self.t_money = None
        self.d_investor_money = dict()
        self.individual_share = None
        self.member_only_expenses = dict()
        self.total_money = None
        self.extra_details_panel = None
        self.item_list = None
        self.individual_share_label = None
        self.total_money_label = None
        self.add_member_window = None
        self.list_box = None
        self.font_list = Database.font_list

        self.profile_values = get_variable_values()
        self.name = self.profile_values['name_idx']
        self.user_email = self.profile_values['user_email']
        self.email_password = self.profile_values['email_password_idx']
        self.phone_number = self.profile_values['phone_number']
        self.upi_id = self.profile_values['upi_id']

        self.theme = self.profile_values['theme'][:-5]  # Remove 'Theme' from Light or Dark
        self.theme_values = get_theme_values(self.profile_values['theme'])

        self.fg_color = self.theme_values['fg_color']
        self.entry_bg_color = self.theme_values['entry_bg_color']
        self.bg_color = self.theme_values['bg_color']
        self.font = self.theme_values['font']
        self.font_size = self.theme_values['font_size']
        self.button_size = int(self.theme_values['button_size'])

        if self.theme == 'Light':
            self.delete_icon = PhotoImage(master=self.main_panel, file="images/dark_delete.png")
            self.edit_icon = PhotoImage(master=self.main_panel, file="images/dark_edit.png")
        elif self.theme == 'Dark':
            self.delete_icon = PhotoImage(master=self.main_panel, file="images/white_delete.png")
            self.edit_icon = PhotoImage(master=self.main_panel, file="images/white_edit.png")

        self.create_new_entry_flag = False
        self.list_of_items_flag = False

        # Start Building the main window
        self.main_panel.title("Share App")
        # Icon of the main window
        self.main_panel.iconbitmap('./images/logo.ico')
        # Creating Menubar
        menu_bar = Menu(self.main_panel, background=self.bg_color, fg=self.fg_color)

        # File menu
        setting_menu = Menu(menu_bar, tearoff=False, background=self.bg_color, fg=self.fg_color)
        menu_bar.add_cascade(label="File", menu=setting_menu)

        setting_menu.add_command(label='Settings', command=lambda: [self.create_setting_window()])
        setting_menu.add_separator()
        # setting_menu.add_command(label="New...", command=lambda: [new_application()])
        setting_menu.add_command(label="Exit", command=lambda: [self.main_panel.destroy()])

        # Main panel's background color
        self.main_panel.config(bg=self.bg_color, menu=menu_bar)
        # Creating content on main window according to settings
        self.create_main_window()
        # Size of the main panel
        self.main_panel.minsize(1050, 185)
        self.main_panel.mainloop()

    def add_members_to_list(self, box):
        for i in box.curselection():
            if box.get(i) not in self.list_of_members:
                self.list_of_members.append(box.get(i))

    def add_members(self):
        if self.event.get() == '':
            messagebox.showwarning(master=self.main_panel, title='Error', message='Please add title for the event')
            return
        self.add_member_window = Toplevel(master=self.main_panel)
        self.add_member_window.title('Select Members for the Event')
        self.add_member_window.geometry('500x500')
        # Icon of add member window
        self.add_member_window.iconbitmap('./images/outline_group_add_black_36dp.ico')

        scrollbar = Scrollbar(self.add_member_window)
        scrollbar.pack(side=RIGHT, fill=Y)

        label = Label(self.add_member_window,
                      text='Select members below',
                      font=(self.font, self.font_size),
                      bg=self.bg_color,
                      fg=self.fg_color,
                      padx=10, pady=15)
        label.pack()

        self.list_box = Listbox(self.add_member_window, selectmode="multiple", yscrollcommand=scrollbar.set)

        self.list_box.config(font=(self.font, self.font_size),
                             bd=5,
                             fg=self.fg_color,
                             bg=self.entry_bg_color)
        self.list_box.pack(padx=10, pady=10, expand=YES, fill="both")

        list_of_members_1 = list(get_members().keys())

        for each_item in range(len(list_of_members_1)):
            if list_of_members_1[each_item] == self.name:
                self.list_box.insert(0, list_of_members_1[each_item])
            else:
                self.list_box.insert(END, list_of_members_1[each_item])
            self.list_box.itemconfig(each_item, bg=self.entry_bg_color)

        # Attach listbox to vertical scrollbar
        scrollbar.config(troughcolor=self.bg_color, command=self.list_box.yview)

        add_members_window_button_frame = Frame(self.add_member_window, bg=self.bg_color)

        Button(master=add_members_window_button_frame,
               bd=0,
               bg=self.bg_color,
               height=30,
               width=30,
               image=self.edit_icon,
               command=lambda: [self.edit_user()]).pack(side='left', padx=10, pady=10)
        Button(master=add_members_window_button_frame,
               bd=0,
               bg=self.bg_color,
               height=30,
               width=30,
               image=self.delete_icon,
               command=lambda: [self.create_confirmation_window()]).pack(side='left', padx=10, pady=10)

        Button(master=add_members_window_button_frame,
               bd=2,
               fg=self.fg_color,
               height=1,
               width=18,
               font=(self.font, self.button_size),
               text='Add New Members',
               bg=self.bg_color,
               command=lambda: [self.entry_new_member()]).pack(side='left', padx=10, pady=10)

        Button(master=add_members_window_button_frame,
               bd=2,
               fg=self.fg_color,
               height=1,
               width=15,
               font=(self.font, self.button_size),
               text='Select Members',
               bg=self.bg_color,
               command=lambda: [self.add_members_to_list(self.list_box),
                                self.create_d_investor_money(),
                                self.destroy_add_member_window()]
               ).pack(side='left', padx=10, pady=10)
        add_members_window_button_frame.pack(side='bottom')

        # Unbinding from main_panel and binding Enter button on add_member_window to Select Members button
        # After this add_member_window will be destroyed hence binding will be removed from Enter
        self.main_panel.unbind('<Return>')
        self.add_member_window.bind('<Return>', lambda event: [
            self.add_members_to_list(self.list_box),
            self.create_d_investor_money(),
            self.destroy_add_member_window()])

        self.add_member_window.config(bg=self.bg_color)
        self.add_member_window.minsize(530, 510)
        self.add_member_window.grab_set()
        # self.add_member_window.bell()
        self.add_member_window.mainloop()

    def destroy_add_member_window(self):
        """In order to add members new_entry_frame will be recreated hence destroy all widgets from it first"""
        if self.create_new_entry_flag:
            for widget in self.new_entry_frame.winfo_children():
                widget.destroy()
            self.create_new_entry_flag = False

        if len(self.list_of_members) < 2:
            messagebox.showwarning(master=self.add_member_window, parent=self.add_member_window, title='Error',
                                   message='Minimum two members should be selected')
        else:
            self.list_of_items()
            self.create_new_entry()
            self.add_member_window.destroy()
            
            Label(master=self.taskbar_frame,
                  bg=self.bg_color,
                  fg=self.fg_color,
                  text=f'Members: {len(self.list_of_members)}').grid(row=0, column=2, padx=5, pady=2)

            self.number_list_items_label = Label(master=self.taskbar_frame,
                                                 bg=self.bg_color,
                                                 fg=self.fg_color,
                                                 text=f'Items: {len(self.items)}')
            self.number_list_items_label.grid(row=0, column=3, padx=5, pady=2)

            Button(master=self.first_row_frame,
                   bd=2,
                   fg=self.fg_color,
                   height=1,
                   width=10,
                   font=(self.font, self.button_size),
                   text='Done',
                   bg=self.bg_color,
                   command=self.send_emails).grid(padx=20, pady=5, row=0, column=4)
            self.main_panel.bind('<Return>', lambda event: self.send_emails())

    def create_new_entry(self):
        if not self.create_new_entry_flag:
            self.item = StringVar()
            self.money_var = DoubleVar(value=0)
            self.clicked_user = StringVar(value="Select a Member")
            member_only_expense_flag = BooleanVar(value=True)

            Checkbutton(master=self.new_entry_frame,
                        text='',
                        bg=self.bg_color,
                        onvalue=False,
                        offvalue=True,
                        variable=member_only_expense_flag,
                        command=lambda: [self.clicked_user.set('Paid For') if not member_only_expense_flag.get()
                                         else self.clicked_user.set('Select a Member'),
                                         messagebox.showinfo(master=self.main_panel, title='Share App',
                                                             message="Now paid money will only be included in\n"
                                                                     "selected member's share.")
                                         if not member_only_expense_flag.get() else None]
                        ).grid(padx=5, pady=5, row=0, column=0, sticky=E)

            self.clicked_user_drop = OptionMenu(self.new_entry_frame, self.clicked_user, *self.list_of_members)
            self.clicked_user_drop.config(font=(self.font, self.font_size),
                                          bd=2,
                                          fg=self.fg_color,
                                          justify='right',
                                          bg=self.entry_bg_color)
            self.clicked_user_drop.grid(padx=5, pady=5, row=0, column=1, sticky=E)
            self.clicked_user_drop["menu"]["background"] = self.entry_bg_color
            self.clicked_user_drop["menu"]["font"] = (self.font, self.font_size)
            self.clicked_user_drop["menu"]["activeborderwidth"] = '2'
            for x in range(int(self.clicked_user_drop['menu'].index('end')) + 1):
                self.clicked_user_drop['menu'].entryconfig(x, font=(self.font, self.font_size))
                self.clicked_user_drop.children['menu'].entryconfig(x, foreground=self.fg_color)

            Label(master=self.new_entry_frame,
                  text="Paid",
                  font=(self.font, self.font_size),
                  fg=self.fg_color,
                  bg=self.bg_color).grid(padx=5, pady=5, row=0, column=2, sticky=E)
            Entry(master=self.new_entry_frame,
                  font=(self.font, self.font_size),
                  textvariable=self.money_var,
                  bd=5,
                  fg=self.fg_color,
                  bg=self.entry_bg_color,
                  justify='right').grid(padx=5, pady=5, row=0, column=3, sticky=E)
            Label(master=self.new_entry_frame,
                  text="For",
                  font=(self.font, self.font_size),
                  fg=self.fg_color,
                  bg=self.bg_color).grid(padx=5, pady=5, row=0, column=4, sticky=E)
            Entry(master=self.new_entry_frame,
                  font=(self.font, self.font_size),
                  textvariable=self.item,
                  bd=5,
                  fg=self.fg_color,
                  bg=self.entry_bg_color,
                  justify='right').grid(padx=5, pady=5, row=0, column=5, sticky=E)

            def reset_new_entry():
                self.money_var.set(0)
                self.item.set('')
                self.clicked_user.set("Select a Member")
                member_only_expense_flag.set(value=True)

            Button(self.new_entry_frame,
                   bd=2,
                   fg=self.fg_color,
                   height=1,
                   width=10,
                   font=(self.font, self.button_size),
                   text='Submit',
                   bg=self.bg_color,
                   command=lambda: reset_new_entry()
                   if self.member_input(member_only_expense_flag.get(), self.clicked_user, self.money_var) else None)\
                .grid(padx=5, pady=5, row=0, column=6, sticky=E)

            self.create_new_entry_flag = True

    def create_star_label(self):
        self.star_label = Label(self.taskbar_frame,
                                bg=self.bg_color,
                                fg=self.fg_color,
                                text="*: Paid Money is not included in Total Paid Money")
        self.star_label.grid(row=0, column=4, padx=5, pady=2)

    def list_of_items(self):
        """If list of item is already created then this function won't create another one.
           If more members are selected then it will change individual_share in else part"""
        if not self.list_of_items_flag:
            self.list_of_items_frame = Frame(self.main_panel, bg=self.entry_bg_color)
            Label(master=self.list_of_items_frame,
                  text="List of event's expenses",
                  font=(self.font, self.font_size),
                  fg=self.fg_color,
                  bg=self.entry_bg_color,
                  name='list_label').pack(side='top', fill=X)
            self.item_list = ttk.Treeview(self.list_of_items_frame)
            style = ttk.Style()
            style.configure("Treeview", foreground=self.fg_color, background=self.bg_color)
            style.configure("Treeview.Heading", background="black", foreground='#00337f', font=8)
            style.configure("Treeview.Heading", borderwidth=8)

            self.item_list['columns'] = ('S.No.', "member's_name", "Paid For", "Paid", "Included")

            self.item_list.column("#0", width=0, stretch=NO)
            self.item_list.column('S.No.', anchor=CENTER, width=40)
            self.item_list.column("member's_name", anchor=CENTER, width=80)
            self.item_list.column("Paid For", anchor=CENTER, width=120)
            self.item_list.column("Paid", anchor=CENTER, width=80)
            self.item_list.column("Included", anchor=CENTER, width=80)

            self.item_list.heading("#0", text="", anchor=CENTER)
            self.item_list.heading('S.No.', text='S.No.', anchor=CENTER)
            self.item_list.heading("member's_name", text='Name', anchor=CENTER)
            self.item_list.heading("Paid For", text='Paid For', anchor=CENTER)
            self.item_list.heading("Paid", text='Money', anchor=CENTER)
            self.item_list.heading("Included", text='Included', anchor=CENTER)

            self.item_list.pack(side='top', fill=BOTH, expand=True)
            self.list_of_items_frame.pack(padx=50, pady=50, side='left', fill=BOTH, expand=True)

            self.extra_details_panel = Frame(self.main_panel, bg=self.bg_color)

            self.total_money = DoubleVar(value=0.0)
            self.total_money_label = Label(master=self.extra_details_panel,
                                           text=f"Total Paid Money: {self.total_money.get()}",
                                           font=(self.font, self.font_size),
                                           fg=self.fg_color,
                                           bg=self.bg_color)
            self.total_money_label.grid(row=0, column=0, padx=(0, 50), pady=4, sticky=W)

            self.individual_share = DoubleVar(value=0.0)
            self.individual_share_label = Label(master=self.extra_details_panel,
                                                text=f"Individual Share: {self.individual_share.get()}",
                                                font=(self.font, self.font_size),
                                                fg=self.fg_color,
                                                bg=self.bg_color)
            self.individual_share_label.grid(row=1, column=0, padx=(0, 50), pady=4, sticky=W)

            self.extra_details_panel.pack(padx=10, pady=10, side='left')
            self.main_panel.minsize(1050, 550)
            self.list_of_items_flag = True
        else:
            self.individual_share.set(round(self.total_money.get() / len(self.list_of_members), 2))
            self.individual_share_label.config(text=f"Individual Share: {self.individual_share.get()}")

    def edit_user(self):
        edit_user_window = Toplevel(master=self.main_panel)
        edit_user_window.title("Edit Member's Details")
        # Icon of the edit member window
        edit_user_window.iconbitmap('./images/edit.ico')
        edit_user_window.config(bg=self.bg_color)

        def set_value(*args):
            new_email.set(users_dict[selected_user.get()])
            selected_user_email_entry.config(textvariable=new_email)

        users_dict = get_members()
        selected_user = StringVar(value="Select a User")
        selected_user.trace('w', set_value)
        new_email = StringVar(value='')

        Label(master=edit_user_window,
              fg=self.fg_color,
              bg=self.bg_color,
              font=(self.font, self.font_size),
              text='Select User:').grid(row=0, column=0, padx=10, pady=5, sticky=E)

        selected_user_drop = OptionMenu(edit_user_window, selected_user, *list(users_dict.keys()))
        selected_user_drop.config(font=(self.font, self.font_size),
                                  bd=2,
                                  fg=self.fg_color,
                                  bg=self.entry_bg_color,
                                  justify='right')
        selected_user_drop.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        selected_user_drop["menu"]["background"] = self.entry_bg_color
        selected_user_drop["menu"]["font"] = (self.font, self.font_size)
        selected_user_drop["menu"]["activeborderwidth"] = '1'
        for x in range(int(selected_user_drop['menu'].index('end')) + 1):
            selected_user_drop['menu'].entryconfig(x, font=(self.font, self.font_size))
            selected_user_drop.children['menu'].entryconfig(x, foreground=self.fg_color)

        Label(master=edit_user_window,
              fg=self.fg_color,
              bg=self.bg_color,
              font=(self.font, self.font_size),
              text='Email:').grid(row=1, column=0, padx=10, pady=5, sticky=E)

        selected_user_email_entry = Entry(master=edit_user_window,
                                          font=(self.font, self.font_size),
                                          width=22,
                                          textvariable=new_email,
                                          bd=5,
                                          fg=self.fg_color,
                                          bg=self.entry_bg_color,
                                          justify='right')
        selected_user_email_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        Button(master=edit_user_window,
               bd=1,
               fg=self.fg_color,
               font=(self.font, self.button_size),
               text='Save',
               height=1,
               width=10,
               bg=self.bg_color,
               command=lambda: [Database.update_email(selected_user.get(), new_email.get())
                                if selected_user.get() != self.name
                                else messagebox.showwarning(
                   master=edit_user_window, parent=edit_user_window,
                   title='Error',
                   message=f"You can not change Email of default user '{self.name}'"),
                                edit_user_window.destroy()]).grid(row=2, column=0, columnspan=2, pady=10)

        edit_user_window.resizable(False, False)
        edit_user_window.bind('<Return>', lambda event: [Database.update_email(selected_user.get(), new_email.get()),
                                                         edit_user_window.destroy()])
        edit_user_window.grab_set()
        edit_user_window.mainloop()

    def create_confirmation_window(self):
        users = [self.list_box.get(i) for i in self.list_box.curselection()]
        if self.name in users:
            messagebox.showwarning(master=self.add_member_window, parent=self.add_member_window, title='Error',
                                   message=f"You can not remove default user '{self.name}'!")
            return
        if users:
            if messagebox.askyesno(master=self.add_member_window,
                                   parent=self.add_member_window,
                                   title='Delete a Member',
                                   message=f"Are you sure, you want to remove '{', '.join(users)}'!"):
                for user in users:
                    Database.remove_member(user)
                    self.list_box.delete(self.list_box.get(0, END).index(user))

    def entry_new_member(self):
        self.new_member_window = Toplevel(master=self.main_panel)
        self.new_member_window.title("Add New Member")
        # Icon of the new member window
        self.new_member_window.iconbitmap('images/add_members.ico')
        # Main panel's background color
        self.new_member_window.config(bg=self.bg_color)

        user_name = StringVar()
        email = StringVar()

        top_frame = Frame(self.new_member_window, bg=self.bg_color)
        top_frame.pack(side='top')

        # Username Entry
        label_frame = Frame(top_frame, bg=self.bg_color)
        label_frame.pack(side='left')

        Label(label_frame, text="Member's Name: ", font=(self.font, self.font_size), fg=self.fg_color,
              bg=self.bg_color).grid(row=0, column=0, padx=5, pady=5, sticky=E)
        Label(label_frame, text="Email: ", font=(self.font, self.font_size), fg=self.fg_color,
              bg=self.bg_color).grid(row=1, column=0, padx=5, pady=5, sticky=E)

        # Password entry
        entry_frame = Frame(top_frame, bg=self.bg_color)
        entry_frame.pack(side='right')

        Entry(entry_frame, font=(self.font, self.font_size), textvariable=user_name, bd=5, fg=self.fg_color,
              bg=self.entry_bg_color, justify='right').pack(padx=5, pady=5)
        Entry(entry_frame, font=(self.font, self.font_size), textvariable=email, bd=5, fg=self.fg_color,
              bg=self.entry_bg_color, justify='right').pack(padx=5, pady=5)

        # Submit button
        button_frame = Frame(self.new_member_window, bg=self.bg_color)
        button_frame.pack(side='bottom')
        Button(master=button_frame,
               bd=2,
               height=1,
               width=10,
               fg=self.fg_color,
               font=(self.font, self.button_size),
               text='Submit',
               bg=self.bg_color,
               command=lambda: [self.insert_new_member(user_name, email)]).pack(pady=10)

        self.new_member_window.grab_set()
        self.new_member_window.bind('<Return>', lambda event: [self.insert_new_member(user_name, email)])
        self.new_member_window.resizable(False, False)
        self.new_member_window.mainloop()

    def insert_new_member(self, user_name, email):
        warning_label = None
        if user_name.get() == '' or email.get() == '':
            if warning_label is not None:
                warning_label.destroy()
            warning_label = Label(master=self.new_member_window,
                                  text='Username or email is not valid',
                                  font=(self.font, 10),
                                  bg=self.bg_color,
                                  fg='red')
            warning_label.pack(padx=4, pady=4, side='top', fill='x')
        elif user_name.get() in get_members().keys():
            if warning_label is not None:
                warning_label.destroy()
            warning_label = Label(master=self.new_member_window,
                                  text='Username is already exits',
                                  font=(self.font, 10),
                                  bg=self.bg_color,
                                  fg='red')
            warning_label.pack(padx=4, pady=4, side='top', fill='x')
        elif email.get() in get_members().values():
            if warning_label is not None:
                warning_label.destroy()
            warning_label = Label(master=self.new_member_window,
                                  text="Email is already in use",
                                  font=(self.font, 10),
                                  bg=self.bg_color,
                                  fg='red')
            warning_label.pack(padx=4, pady=4, side='top', fill='x')
        else:
            user_name = user_name.get()
            email = email.get()
            Database.insert_member(user_name, email)

            self.list_box.insert(END, user_name)
            self.new_member_window.destroy()

    def create_d_investor_money(self):
        for member in self.list_of_members:
            if member not in self.d_investor_money.keys():
                self.d_investor_money[member] = 0

    def member_input(self, bool_var, username, money_var):
        """bool_var: Boolean value (True if share is included False otherwise)
           This function returns a boolean value to reset entries"""
        try:
            member = username.get()
            money = money_var.get()
            if bool_var:
                self.total_money.set(self.total_money.get() + money)
                self.d_investor_money[member] += money
                self.item_to_list(username, self.item, self.money_var, "Yes")
                self.total_money_label.config(text=f"Total Paid Money: {self.total_money.get()}")
                self.star_label.destroy() if self.star_label else None
            else:
                self.member_only_expenses[member] = money if member not in self.member_only_expenses\
                    else self.member_only_expenses[member] + money
                self.item_to_list(username, self.item, self.money_var, "No")
                self.total_money_label.config(text=f"Total Paid Money: {self.total_money.get()}*")
                self.create_star_label()

            self.item_list.insert(parent='', index='end', text='', values=(len(self.items), *self.items[-1]))

            self.individual_share.set(round(self.total_money.get() / len(self.list_of_members), 2))
            self.individual_share_label.config(text=f"Individual Share: {self.individual_share.get()}")
            return True
        except TclError:
            messagebox.showwarning(master=self.main_panel, title='Error', message='Paid section expects decimal values')
            return False
        except KeyError:
            messagebox.showwarning(master=self.main_panel, title='Error', message='Please select a member')
            return False

    def create_setting_contents(self, flag):
        if flag == self.current_page:
            return
        try:
            for widget in self.right_top_frame.winfo_children():
                widget.destroy()
        except AttributeError:
            pass

        if flag == 'profile':
            self.current_page = 'profile'
            # Darken the select field on the left_frame
            self.left_profile_frame.config(bg='#789bff')
            # changing label's color to the same as frame
            self.left_profile_frame.winfo_children()[0].config(bg='#789bff')
            # changing theme frame and it's components to left frame color
            self.left_theme_frame.config(bg=self.bg_color)
            # changing label's color to the same as frame
            self.left_theme_frame.winfo_children()[0].config(bg=self.bg_color)

            Label(self.right_top_frame, text='Name', font=(self.font, self.font_size), fg=self.fg_color,
                  bg=self.bg_color).grid(row=0, column=0, padx=4, pady=(15, 4), sticky=E)

            Entry(self.right_top_frame, font=(self.font, self.font_size), textvariable=self.name_var, bd=5, width=25,
                  bg=self.entry_bg_color, fg=self.fg_color, justify='right').grid(row=0, column=1, padx=4, pady=(15, 4))

            Label(self.right_top_frame, text='Email', font=(self.font, self.font_size), fg=self.fg_color,
                  bg=self.bg_color).grid(row=1, column=0, padx=4, pady=4, sticky=E)

            Entry(self.right_top_frame, font=(self.font, self.font_size), textvariable=self.email_var, bd=5, width=25,
                  bg=self.entry_bg_color, fg=self.fg_color, justify='right').grid(row=1, column=1, padx=4, pady=4)

            Label(self.right_top_frame, text='Phone No.', font=(self.font, self.font_size), fg=self.fg_color,
                  bg=self.bg_color).grid(row=2, column=0, padx=4, pady=4, sticky=E)

            Entry(self.right_top_frame, font=(self.font, self.font_size), textvariable=self.phone_number_var, bd=5,
                  width=25, bg=self.entry_bg_color, fg=self.fg_color,
                  justify='right').grid(row=2, column=1, padx=4, pady=4)

            Label(self.right_top_frame, text='UPI IDs', font=(self.font, self.font_size), fg=self.fg_color,
                  bg=self.bg_color).grid(row=3, column=0, padx=4, pady=4, sticky=E)

            Entry(self.right_top_frame, font=(self.font, self.font_size), textvariable=self.upi_id_var, bd=5, width=25,
                  bg=self.entry_bg_color, fg=self.fg_color, justify='right').grid(row=3, column=1, padx=4, pady=4)

            Label(self.right_top_frame, text='App Password', font=(self.font, self.font_size), fg=self.fg_color,
                  bg=self.bg_color).grid(row=4, column=0, padx=4, pady=4, sticky=E)

            Entry(self.right_top_frame, font=(self.font, self.font_size), textvariable=self.email_password_var, bd=5,
                  width=25, bg=self.entry_bg_color, fg=self.fg_color,
                  justify='right').grid(row=4, column=1, padx=4, pady=4)

            link_label = Label(master=self.right_top_frame,
                               text='Follow this link to setup your app password using the same email field in Email',
                               font=(self.font, 10, 'underline'),
                               fg='#4a52e8',
                               bg=self.bg_color,
                               name='link_label',
                               cursor="hand2")
            link_label.grid(row=5, column=0, columnspan=3, padx=8, pady=4)
            link_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://myaccount.google.com/apppasswords"))

            Label(self.right_top_frame, text='QR Codes', font=(self.font, self.font_size), fg=self.fg_color,
                  bg=self.bg_color).grid(row=6, column=0, padx=4, pady=4, sticky=E)

            if os.path.exists(os.path.join(app_data_location, 'QR_Codes.png')):
                browse_qr_codes_button_message = "Change QR Codes"
            else:
                browse_qr_codes_button_message = "Browse QR Codes"
            browse_qr_codes_button = Button(master=self.right_top_frame,
                                            bd=1,
                                            fg=self.fg_color,
                                            font=(self.font, self.button_size),
                                            height=1,
                                            width=22,
                                            text=browse_qr_codes_button_message,
                                            bg=self.bg_color,
                                            command=lambda: [
                                                self.new_qr_codes.set(','.join(browse_qr_codes())),
                                                browse_qr_codes_button.config(text='Change QR Codes')
                                                if self.new_qr_codes.get() != '' else None])
            browse_qr_codes_button.grid(row=6, column=1, padx=4, pady=4)

        elif flag == 'theme':
            self.current_page = 'theme'
            # darken the select field on the left_frame
            self.left_theme_frame.config(bg='#789bff')
            # changing label's color to the same as frame
            self.left_theme_frame.winfo_children()[0].config(bg='#789bff')
            # changing profile frame and it's components to left frame color
            self.left_profile_frame.config(bg=self.bg_color)
            # changing label's color to the same as frame
            self.left_profile_frame.winfo_children()[0].config(bg=self.bg_color)

            Label(master=self.right_top_frame,
                  text="Theme",
                  font=(self.font, self.font_size),
                  fg=self.fg_color,
                  bg=self.bg_color).grid(row=0, column=0, padx=10, pady=4, sticky=E)

            theme_option_menu = OptionMenu(self.right_top_frame, self.theme_value, *['Light', 'Dark'])
            theme_option_menu.config(font=(self.font, self.font_size),
                                     bd=2,
                                     fg=self.fg_color,
                                     bg=self.entry_bg_color)
            theme_option_menu.grid(padx=10, pady=5, row=0, column=1, sticky=W)
            theme_option_menu["menu"]["background"] = self.entry_bg_color
            theme_option_menu["menu"]["font"] = (self.font, self.font_size)
            for x in range(int(theme_option_menu['menu'].index('end')) + 1):
                theme_option_menu['menu'].entryconfig(x, font=(self.font, self.font_size))
                theme_option_menu.children['menu'].entryconfig(x, foreground=self.fg_color)
            theme_option_menu["menu"]["activeborderwidth"] = '2'

            Label(master=self.right_top_frame, text="Font", font=(self.font, self.font_size), fg=self.fg_color,
                  bg=self.bg_color).grid(row=1, column=0, padx=10, pady=4, sticky=E)

            font_option_menu = OptionMenu(self.right_top_frame, self.font_value_var, *self.font_list)
            font_option_menu.config(font=(self.font, self.font_size),
                                    bd=2,
                                    fg=self.fg_color,
                                    bg=self.entry_bg_color)
            font_option_menu.grid(padx=10, pady=5, row=1, column=1, sticky=W)
            font_option_menu["menu"]["background"] = self.entry_bg_color
            font_option_menu["menu"]["font"] = (self.font, self.font_size)
            for x in range(int(font_option_menu['menu'].index('end')) + 1):
                font_option_menu['menu'].entryconfig(x, font=(self.font_list[x], self.font_size))
                font_option_menu.children['menu'].entryconfig(x, foreground=self.fg_color)
            font_option_menu["menu"]["activeborderwidth"] = '2'

    def change_settings(self, window_destroy):
        theme_changes = []
        profile_changes = []
        if self.theme_values['font'] != self.font_value_var.get() or self.theme_value.get() != self.theme:
            theme_changes.append((self.theme_value.get(), 'font', self.font_value_var.get()))
        for x, y in [('name_idx', self.name_var.get()),
                     ('user_email', self.email_var.get()),
                     ('phone_number', self.phone_number_var.get()),
                     ('upi_id', self.upi_id_var.get()),
                     ('email_password_idx',
                      self.email_password_var.get())]:
            if self.profile_values[x] != y:
                profile_changes.append((x, y))

        if theme_changes:
            theme, _font, font_value = theme_changes[0]
            self.theme = theme

            # Updating theme value in database
            self.profile_values['theme'] = self.theme + 'Theme'
            Database.update_profile_value('theme', self.profile_values['theme'])

            # updating buttons
            if self.theme == 'Light':
                self.delete_icon = PhotoImage(master=self.main_panel, file="images/dark_delete.png")
                self.edit_icon = PhotoImage(master=self.main_panel, file="images/dark_edit.png")
            elif self.theme == 'Dark':
                self.delete_icon = PhotoImage(master=self.main_panel, file="images/white_delete.png")
                self.edit_icon = PhotoImage(master=self.main_panel, file="images/white_edit.png")

            # Updating font value in current theme and getting all theme_values from current theme
            Database.update_theme_value(self.profile_values['theme'], _font, font_value)
            self.theme_values = get_theme_values(self.profile_values['theme'])
            self.theme_values[_font] = font_value
            # All changes are made
            theme_changes.clear()

            # Changing profile values from current values
            self.fg_color = self.theme_values['fg_color']
            self.entry_bg_color = self.theme_values['entry_bg_color']
            self.bg_color = self.theme_values['bg_color']
            self.font = self.theme_values['font']

            # Changing theme of currently open widgets
            self.main_panel.config(bg=self.bg_color)
            for widget in self.main_panel.winfo_children():
                if widget.winfo_class() == 'Label':  # This is a warning label, we don't want to change fg color
                    widget.config(font=(self.font, self.font_size), bg=self.bg_color)
                elif widget.winfo_class() == 'Button':  # Setup Profile Button
                    widget.config(font=(self.font, self.button_size), bg=self.bg_color, fg=self.fg_color)
                elif widget.winfo_class() == 'Menu':
                    widget.winfo_children()[0].config(background=self.bg_color, fg=self.fg_color)
                elif widget.winfo_class() == 'Frame':
                    widget.config(bg=self.bg_color)
                    # We don't want to change font value for task_bar frame's widgets
                    if str(widget).split('.')[-1] == 'task_bar':
                        for child_widget in widget.winfo_children():
                            child_widget.config(bg=self.bg_color, fg=self.fg_color)
                    else:
                        for child_widget in widget.winfo_children():
                            if str(child_widget).split('.')[-1] == 'list_label':
                                child_widget.config(font=(self.font, self.font_size), bg=self.entry_bg_color,
                                                    fg=self.fg_color)
                            if child_widget.winfo_class() == 'Label' and\
                                    str(child_widget).split('.')[-1] != 'list_label':
                                child_widget.config(font=(self.font, self.font_size), bg=self.bg_color,
                                                    fg=self.fg_color)
                            elif child_widget.winfo_class() == 'Entry':
                                child_widget.config(font=(self.font, self.font_size), fg=self.fg_color,
                                                    bg=self.entry_bg_color)
                            elif child_widget.winfo_class() == 'Button':
                                child_widget.config(bg=self.bg_color, fg=self.fg_color,
                                                    font=(self.font, self.button_size))
                            elif child_widget.winfo_class() == 'Menubutton':
                                child_widget.config(fg=self.fg_color, bg=self.entry_bg_color,
                                                    font=(self.font, self.font_size))
                                child_widget["menu"]["background"] = self.entry_bg_color
                                child_widget["menu"]["font"] = (self.font, self.font_size)
                                for x in range(int(child_widget['menu'].index('end')) + 1):
                                    child_widget['menu'].entryconfig(x, font=(self.font, self.font_size))
                                    child_widget.children['menu'].entryconfig(x, foreground=self.fg_color)

            for frame in self.setting_window.winfo_children():
                if frame.winfo_class() == 'Frame':
                    border_color = "black" if self.theme == 'Light' else "white"
                    frame.config(bg=self.bg_color, highlightbackground=border_color)
                    for child_widget in frame.winfo_children():
                        # Setting's left frame has two more frames with one label each Profile and Theme
                        if child_widget.winfo_class() == 'Frame':
                            if self.current_page == str(child_widget).split('.')[-1]:
                                child_widget.config(highlightbackground=border_color, bg='#789bff')
                                child_widget.winfo_children()[0].config(font=(self.font, self.font_size),
                                                                        fg=self.fg_color, bg='#789bff')
                            else:
                                child_widget.config(highlightbackground=border_color, bg=self.bg_color)
                                child_widget.winfo_children()[0].config(font=(self.font, self.font_size),
                                                                        fg=self.fg_color, bg=self.bg_color)
                        elif child_widget.winfo_class() == 'Label':
                            if str(child_widget).split('.')[-1] == 'link_label':
                                child_widget.config(bg=self.bg_color)
                            else:
                                child_widget.config(font=(self.font, self.font_size), bg=self.bg_color,
                                                    fg=self.fg_color)
                        elif child_widget.winfo_class() == 'Entry':
                            child_widget.config(font=(self.font, self.font_size), fg=self.fg_color,
                                                bg=self.entry_bg_color)
                        elif child_widget.winfo_class() == 'Button':
                            child_widget.config(bg=self.bg_color, fg=self.fg_color, font=(self.font, self.button_size))
                        elif child_widget.winfo_class() == 'Menubutton':
                            child_widget.config(fg=self.fg_color, bg=self.entry_bg_color,
                                                font=(self.font, self.font_size))
                            child_widget["menu"]["background"] = self.entry_bg_color
                            child_widget["menu"]["font"] = (self.font, self.font_size)
                            for x in range(int(child_widget['menu'].index('end')) + 1):
                                child_widget['menu'].entryconfig(x, font=(self.font, self.font_size))
                                child_widget.children['menu'].entryconfig(x, foreground=self.fg_color)

        if profile_changes:
            for variable, value in profile_changes:
                Database.update_profile_value(variable, value)
                self.profile_values[variable] = value
            profile_changes.clear()

            # Before changing default user's name (self.name) removing email of old user's name from database
            Database.remove_member(self.name) if self.name != self.profile_values['name_idx'] else None
            # Inserting new default user into database
            Database.insert_member(self.profile_values['name_idx'], self.profile_values['user_email'])

            # If self.individual_share_label is created then update self.list_of_members with new default user
            if self.individual_share_label is not None:
                self.list_of_members.remove(self.name)
                self.list_of_members.insert(0, self.profile_values['name_idx'])
                self.clicked_user_drop['menu'].delete(0, END)
                for value in self.list_of_members:
                    self.clicked_user_drop['menu'].add_command(label=value,
                                                               command=lambda V=value: self.clicked_user.set(V))

                # Changing the username in self.d_investor_money
                self.d_investor_money[self.profile_values['name_idx']] = self.d_investor_money[self.name]
                del self.d_investor_money[self.name]

            # Changing profile values from current values
            self.name = self.profile_values['name_idx']
            self.user_email = self.profile_values['user_email']
            self.email_password = self.profile_values['email_password_idx']
            self.phone_number = self.profile_values['phone_number']
            self.upi_id = self.profile_values['upi_id']

            # Recreating main window
            self.create_main_window()

        # Saving QR Codes
        combine_images(self.new_qr_codes.get()) if self.new_qr_codes.get() != '' else None

        if window_destroy:
            self.setting_window.destroy()

    def create_setting_window(self):
        self.setting_window = Toplevel(master=self.main_panel)
        self.setting_window.title('Settings')
        # Icon of the main window
        self.setting_window.iconbitmap('./images/setting.ico')

        border_color = "black" if self.theme == 'Light' else "white"

        left_frame = Frame(master=self.setting_window, bg=self.bg_color, highlightbackground=border_color,
                           highlightthickness=1)
        self.left_profile_frame = Frame(master=left_frame, bg=self.bg_color, highlightbackground=border_color,
                                        highlightthickness=1, name='profile')
        self.left_theme_frame = Frame(master=left_frame, bg=self.bg_color, highlightbackground=border_color,
                                      highlightthickness=1, name='theme')

        self.left_profile_frame.pack(side=TOP, fill=BOTH)
        self.left_theme_frame.pack(side=TOP, fill=BOTH)

        Label(master=self.left_profile_frame,
              bg=self.bg_color,
              fg=self.fg_color,
              font=(self.font, self.font_size),
              text='Profile').grid(row=0, column=0, padx=20, pady=10, sticky=N)

        # Bind the create profile function to the frame and every widget (one label widget)
        # Saving theme values in local variables
        self.left_profile_frame.bind('<Button-1>', lambda event: [self.create_setting_contents('profile'),
                                                                  self.font_value_var.set(self.font_value_var.get()),
                                                                  self.theme_value.set(self.theme_value.get())])
        [widget.bind('<Button-1>', lambda event: [self.create_setting_contents('profile'),
                                                  self.font_value_var.set(self.font_value_var.get()),
                                                  self.theme_value.set(self.theme_value.get())])
         for widget in self.left_profile_frame.winfo_children()]

        Label(master=self.left_theme_frame,
              bg=self.bg_color,
              fg=self.fg_color,
              font=(self.font, self.font_size),
              text='Appearance').grid(row=1, column=0, padx=20, pady=10, sticky=N)

        # Bind the create theme page function to the frame and every widget (one label widget)
        # Saving profile values in local variables
        self.left_theme_frame.bind('<Button-1>', lambda event: [self.create_setting_contents('theme'),
                                                                self.name_var.set(self.name_var.get()),
                                                                self.email_var.set(self.email_var.get()),
                                                                self.phone_number_var.set(self.phone_number_var.get()),
                                                                self.upi_id_var.set(self.upi_id_var.get()),
                                                                self.email_password_var.set(
                                                                    self.email_password_var.get())])
        [widget.bind('<Button-1>', lambda event: [self.create_setting_contents('theme'),
                                                  self.name_var.set(self.name_var.get()),
                                                  self.email_var.set(self.email_var.get()),
                                                  self.phone_number_var.set(self.phone_number_var.get()),
                                                  self.upi_id_var.set(self.upi_id_var.get()),
                                                  self.email_password_var.set(self.email_password_var.get())])
         for widget in self.left_theme_frame.winfo_children()]

        right_frame = Frame(master=self.setting_window, bg=self.bg_color,
                            highlightbackground=border_color, highlightthickness=1)
        self.right_top_frame = Frame(master=self.setting_window, bg=self.bg_color,
                                     highlightbackground=border_color, highlightthickness=1)

        self.right_bottom_frame = Frame(master=self.setting_window, bg=self.bg_color,
                                        highlightbackground=border_color, highlightthickness=1)

        # default page in setting window
        self.name_var = StringVar(value=self.name)
        self.email_var = StringVar(value=self.user_email)
        self.email_password_var = StringVar(value=self.email_password)
        self.phone_number_var = StringVar(value=self.phone_number)
        self.upi_id_var = StringVar(value=self.upi_id) if self.upi_id not in ['Type comma separated upi ids', ''] \
            else StringVar(value='Type comma separated upi ids')

        self.font_value_var = StringVar(value=self.font)
        self.theme_value = StringVar(value=self.theme)

        self.current_page = None
        self.create_setting_contents('profile')

        # Buttons
        Button(master=self.right_bottom_frame,
               bd=2,
               fg=self.fg_color,
               font=(self.font, self.button_size),
               text='Cancel',
               height=1,
               width=10,
               bg=self.bg_color,
               command=lambda: [self.setting_window.destroy()]
               ).pack(side=RIGHT, padx=4, pady=10)
        Button(master=self.right_bottom_frame,
               bd=2,
               fg=self.fg_color,
               font=(self.font, self.button_size),
               text='Apply',
               height=1,
               width=10,
               bg=self.bg_color,
               command=lambda: [self.change_settings(window_destroy=False)]).pack(side=RIGHT, padx=4, pady=10)
        Button(master=self.right_bottom_frame,
               bd=2,
               fg=self.fg_color,
               font=(self.font, self.button_size),
               text='Ok',
               height=1,
               width=10,
               bg=self.bg_color,
               command=lambda: [self.change_settings(window_destroy=True)]).pack(side=RIGHT, padx=4, pady=10)

        left_frame.pack(side=LEFT, fill=Y)
        right_frame.pack(side=LEFT)
        self.right_top_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.right_bottom_frame.pack(side=TOP, fill=X)

        # Configure setting_window
        self.setting_window.config(bg=self.bg_color)
        self.setting_window.minsize(750, 400)
        self.setting_window.grab_set()
        self.setting_window.mainloop()

    def item_to_csv(self, list_name):
        users = []
        item_names = []
        items_money = []
        included = []
        for user, item, mon, bool_var in self.items:
            users.append(user)
            item_names.append(item)
            items_money.append(mon)
            included.append(bool_var)

        # For those members whose entry has not been created once.
        for member in self.list_of_members:
            if member not in users:
                users.append(member)
                item_names.append('--')
                items_money.append(0)
                included.append('Yes')

        if not os.path.exists(os.path.join(app_data_location, 'items')):
            os.mkdir(os.path.join(app_data_location, 'items'))
        with open(os.path.join(app_data_location, 'items', list_name), 'w') as out:
            out.write('S.No.,Paid By,Item Names,Item Money,Included\n')
            for j in range(len(item_names)):
                out.write(str(j + 1) + ',' + users[j] + ',' + item_names[j] + ',' + str(items_money[j]) + ',' +
                          included[j] + '\n')

    def item_to_list(self, name, item, mon, bool_var):
        user = name.get()
        item_msg = item.get()
        mon_msg = mon.get()
        if item_msg == '':
            self.items.append((user, 'Not Mentioned', mon_msg, bool_var))
        else:
            self.items.append((user, item_msg, mon_msg, bool_var))
        self.number_list_items_label.config(text=f'Items: {len(self.items)}')

    def send_emails(self):
        if not self.items:
            messagebox.showwarning(master=self.main_panel, title='Error', message='Please add some items')
            return
        event_name = self.event.get()
        if event_name == '':
            messagebox.showwarning(master=self.main_panel, title='Error', message='Please add title for the event')
            return
        share = self.total_money.get() / len(self.d_investor_money)
        p4 = ''
        phone = self.phone_number
        phone_pay_upi, g_pay_upi, paytm_upi = get_upi_ids(self.upi_id)
        csv_name = item_name(event_name)
        self.item_to_csv(csv_name)

        done_window = Toplevel(master=self.main_panel)
        done_window.config(bg=self.bg_color)
        done_window.title('Done')
        done_window.iconbitmap('./images/done.ico')
        done_window.minsize(700, 200)

        first_frame = Frame(done_window, bg=self.bg_color)
        done_image = PhotoImage(master=self.main_panel, file='./images/done.png')
        Label(master=first_frame,
              image=done_image,
              bg=self.bg_color).grid(row=0, column=0, sticky="nsew")
        progress_label = Label(master=first_frame,
                               text='Sending Emails',
                               font=(self.font, self.font_size),
                               fg=self.fg_color,
                               bg=self.bg_color)
        progress_label.grid(row=0, column=1, sticky="nsew")
        first_frame.pack(side='top', pady=10)

        second_frame = Frame(master=done_window, bg=self.bg_color)
        second_frame.pack(side='top', pady=10)

        third_frame = Frame(done_window, bg=self.bg_color)
        new_app = Button(master=third_frame,
                         bd=1,
                         fg=self.fg_color,
                         width=15,
                         font=(self.font, self.button_size),
                         text='Fill a new one',
                         bg=self.bg_color,
                         command=lambda: [self.main_panel.destroy(), new_application()])

        close_button = Button(master=third_frame,
                              bd=1,
                              fg=self.fg_color,
                              width=15,
                              font=(self.font, self.button_size),
                              text='Close',
                              bg=self.bg_color,
                              command=lambda: [self.main_panel.destroy(), conn.close()])
        third_frame.pack(side='top', pady=25)

        # Progress bar
        progress_var = DoubleVar(value=0.0)
        ttk.Progressbar(master=second_frame,
                        variable=progress_var,
                        orient=HORIZONTAL,
                        length=500,
                        mode='determinate').grid(row=0, column=0, sticky="nsew")
        percentage_process = Label(master=second_frame, fg=self.fg_color, bg=self.bg_color, font=(self.font, 10),
                                   text=f'{progress_var.get()}%')
        percentage_process.grid(row=0, column=1, sticky="nsew")

        # Updating done_window window to display initial stage
        done_window.update()

        members_email = get_members()
        for mem in self.d_investor_money:
            if mem == self.name:
                continue
            msg = MIMEMultipart()
            msg['Subject'] = f"Your share to pay in {event_name}"
            msg['From'] = self.user_email
            msg['To'] = members_email[mem]

            ctype, encoding = mimetypes.guess_type(csv_name)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"

            maintype, subtype = ctype.split("/", 1)

            with open(os.path.join(app_data_location, 'items', csv_name), "rb") as fp:
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())

            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=csv_name)
            msg.attach(attachment)

            if mem not in self.member_only_expenses:
                member_share = share - self.d_investor_money[mem]
                member_share_message = ''
                p4 += f'<br/>{mem} will give you {round(member_share, 2)}&#8377;' if member_share > 0\
                    else p4 + f'<br/>You have to give {round(-1 * member_share, 2)}&#8377; to {mem}'
            else:
                member_share = share - self.d_investor_money[mem] + self.member_only_expenses[mem]
                member_share_message = f"""{self.name} spent {self.member_only_expenses[mem]}&#8377; 
                on behalf of you"""
                p4 += f'<br/>{mem} will give you {round(member_share, 2)}&#8377;' if member_share > 0\
                    else p4 + f'<br/>You have to give {round(-1 * member_share, 2)}&#8377; to {mem}'
                p4 += f". You have spent {self.member_only_expenses[mem]} on behalf of {mem}"
            if member_share > 0:
                try:  # If QR_Codes doesn't exit
                    qr_code_line_1 = """<p style="margin: 0; font-size: 14px;"><em><strong>QR Codes are given below
                     to make payment</strong></em></p>"""
                    qr_code_line_2 = """<div align="center" style="line-height:10px"><img src="cid:qrcode"
                     style="display: block; height: auto; border: 0; width: 325px; max-width: 100%;" width="325"/>
                     </div>"""
                    qr_code = MIMEImage(open(os.path.join(app_data_location, 'QR_Codes.png'), 'rb').read())
                    qr_code.add_header('Content-ID', '<qrcode>')
                    msg.attach(qr_code)
                    pay_message = open('messages/pay_money_message.html') \
                        .read().format(v1=self.total_money.get(),
                                       v2=round(share, 2),
                                       v3=self.d_investor_money[mem],
                                       member_share_message=member_share_message,
                                       v4=round(member_share, 2),
                                       v5=self.name,
                                       phone=phone,
                                       phone_pay_upi=phone_pay_upi,
                                       g_pay_upi=g_pay_upi,
                                       paytm_upi=paytm_upi,
                                       qr_code_line_1=qr_code_line_1,
                                       qr_code_line_2=qr_code_line_2)
                    msg_body = MIMEText(pay_message, 'html')
                except FileNotFoundError:
                    pay_message = open('messages/pay_money_message.html') \
                        .read().format(v1=self.total_money.get(),
                                       v2=round(share, 2),
                                       v3=self.d_investor_money[mem],
                                       member_share_message=member_share_message,
                                       v4=round(member_share, 2),
                                       v5=self.name,
                                       phone=phone,
                                       phone_pay_upi=phone_pay_upi,
                                       g_pay_upi=g_pay_upi,
                                       paytm_upi=paytm_upi,
                                       qr_code_line_1="",
                                       qr_code_line_2="")
                    msg_body = MIMEText(pay_message, 'html')

            else:
                receive_money_message = open('messages/receive_money_message.html') \
                    .read().format(v1=self.total_money.get(),
                                   v2=round(share, 2),
                                   v3=self.d_investor_money[mem],
                                   member_share_message=member_share_message,
                                   v4=self.name,
                                   v5=round(-1 * member_share, 2))

                msg_body = MIMEText(receive_money_message, 'html')

            logo = MIMEImage(open('./images/logo.png', 'rb').read())
            logo.add_header('Content-ID', '<logo>')
            msg.attach(logo)

            msg.attach(msg_body)

            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(self.user_email, self.email_password)
                    smtp.send_message(msg)

                # Updating progress bar
                progress_var.set(progress_var.get() + 100/len(self.d_investor_money))
                percentage_process.config(text=f'{round(progress_var.get(), 2)}%')
                done_window.update()
            except Exception:
                messagebox.showwarning(master=done_window, parent=done_window, title='Error',
                                       message='You are not connected to internet!')
                done_window.destroy()
                return

        d_msg = MIMEMultipart()
        d_msg['Subject'] = f"Share in {event_name}"
        d_msg['From'] = self.user_email
        d_msg['To'] = self.user_email
        d_msg.attach(attachment)
        receive_email = open('messages/receive_email.html') \
            .read().format(p1=self.total_money.get(),
                           p2=round(share, 2),
                           p3=self.d_investor_money[self.name],
                           p4=p4)
        d_msg_body = MIMEText(receive_email, 'html')
        logo = MIMEImage(open('./images/logo.png', 'rb').read())
        logo.add_header('Content-ID', '<logo>')
        d_msg.attach(logo)

        d_msg.attach(d_msg_body)
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.user_email, self.email_password)
                smtp.send_message(d_msg)

            # Updating progress bar
            progress_var.set(progress_var.get() + 100/len(self.d_investor_money))
            percentage_process.config(text=f'{round(progress_var.get(), 2)}%')
            done_window.update()

            # Putting options
            new_app.grid(row=0, column=0, padx=10, sticky="nsew")
            close_button.grid(row=0, column=1, padx=10, sticky="nsew")
            progress_label.config(text='Emails are sent to members with their share and payment details')
        except Exception:
            messagebox.showwarning(master=done_window, parent=done_window, title='Error',
                                   message='You are not connected to internet!')
            done_window.destroy()
            return

        notification.notify(title="Share App", message="All emails are sent", app_name="Share App",
                            app_icon='./images/logo.ico')

        done_window.grab_set()
        done_window.mainloop()

    def create_main_window(self):
        if self.name == '' or self.user_email == '' or self.email_password == '':
            for widget in self.main_panel.winfo_children():
                if widget.winfo_class() == 'Frame':
                    widget.destroy()  # Destroying new_entry_frame and treeview and extra_details_panel frame
                    self.list_of_items_flag = False
                elif widget.winfo_class() in ['Menu', 'Toplevel']:
                    pass  # We don't want to destroy menubar and setting toplevel window.
                else:
                    widget.destroy()

            Label(master=self.main_panel,
                  text='You have to add your profile details to use the app',
                  font=(self.font, self.font_size),
                  fg='red',
                  bg=self.bg_color).pack(side='top', padx=10, pady=25)
            Button(master=self.main_panel,
                   bd=1,
                   fg=self.fg_color,
                   width=15,
                   font=(self.font, self.button_size),
                   text='Setup Profile',
                   bg=self.bg_color,
                   command=lambda: [self.create_setting_window()]).pack(side='top', padx=10, pady=10)
            self.main_panel.minsize(1050, 175)

            # Since we are using self.individual_share_label and self.first_row_frame to determine whether listbox and
            # add event name label and other widgets are created or not we have to set it None so that after setup
            # profile program does not go to elif statement
            self.individual_share_label = None
            self.first_row_frame = None
        elif self.individual_share_label is not None:
            # If listbox is created and program does not go if statement then we don't want to change anything
            # except taskbar
            self.username_label_taskbar.config(text='User: ' + self.name)
            self.email_taskbar.config(text='Email: ' + self.user_email)
        else:
            # If self.first_row_frame is already created we don't want to recreate it, but we want to update
            # potentially username or email changes in taskbar
            if self.first_row_frame is not None:
                self.username_label_taskbar.config(text='User: ' + self.name)
                self.email_taskbar.config(text='Email: ' + self.user_email)
                return
            for widget in self.main_panel.winfo_children():
                if widget.winfo_class() == 'Frame':
                    widget.destroy()  # Destroying new_entry_frame and treeview and extra_details_panel frame
                    self.list_of_items_flag = False
                elif widget.winfo_class() in ['Menu', 'Toplevel']:
                    pass  # We don't want to destroy menubar and setting toplevel window.
                else:
                    widget.destroy()

            # First Row
            self.first_row_frame = Frame(master=self.main_panel, bg=self.bg_color)
            Label(master=self.first_row_frame,
                  text="Event's Name: ",
                  font=(self.font, self.font_size),
                  bg=self.bg_color,
                  fg=self.fg_color).grid(padx=4, pady=20, row=0, column=0)
            self.event_name_entry = Entry(master=self.first_row_frame,
                                          font=(self.font, self.font_size),
                                          textvariable=self.event,
                                          bd=5,
                                          fg=self.fg_color,
                                          bg=self.entry_bg_color,
                                          justify='right')
            self.event_name_entry.grid(row=0, column=1, padx=4, pady=20)

            Button(master=self.first_row_frame,
                   bd=2,
                   fg=self.fg_color,
                   height=1,
                   width=16,
                   font=(self.font, self.button_size),
                   text='Add Members',
                   bg=self.bg_color,
                   command=lambda: [self.add_members()]).grid(padx=20, pady=20, row=0, column=2)
            self.first_row_frame.pack(side='top')

            # Second Row (Entry Frame)
            self.new_entry_frame = Frame(self.main_panel, bg=self.bg_color)
            self.new_entry_frame.pack(side='top')

            # Button Binding
            self.main_panel.bind('<Return>', lambda event: self.add_members())

            # Creating taskbar
            self.taskbar_frame = Frame(master=self.main_panel, bg=self.bg_color, name='task_bar', relief=RIDGE,
                                       borderwidth=1)
            self.username_label_taskbar = Label(master=self.taskbar_frame,
                                                bg=self.bg_color,
                                                fg=self.fg_color,
                                                text='User: ' + self.name)
            self.username_label_taskbar.grid(row=0, column=0, padx=5, pady=2)
            self.email_taskbar = Label(master=self.taskbar_frame,
                                       bg=self.bg_color,
                                       fg=self.fg_color,
                                       text='Email: ' + self.user_email)
            self.email_taskbar.grid(row=0, column=1, padx=5, pady=2)
            self.taskbar_frame.pack(side=BOTTOM, fill=X)


def new_application():
    App(Tk())


if __name__ == '__main__':
    new_application()
