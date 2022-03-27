import os
import smtplib
import webbrowser
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from tkinter import *
import tkinter.font as font_list
from tkinter import ttk
from plyer import notification
from utils import *


class App:
    def __init__(self):
        self.variables = None
        self.item = None
        self.list_of_items_frame = None
        self.money_var = None
        self.add_event_name_error = None
        self.new_member_window = None
        self.members_email = None
        self.new_entry_frame = None
        self.main_panel = None
        self.first_row_frame = None
        self.event = None
        self.list_of_members = None
        self.items = None
        self.t_money = None
        self.d_investor_money = {}
        self.selected_user_email = None
        self.individual_share = None
        self.total_money = None
        self.extra_details_panel = None
        self.item_list = None
        self.individual_share_label = None
        self.total_money_label = None
        self.reason_entry = None
        self.reason_label = None
        self.enter_money_entry = None
        self.select_member_label = None
        self.clicked_user_drop = None
        self.add_member_window = None
        self.list_box = None
        self.bottom_frame = None
        self.fg_color = 'fg_color'
        self.button_bg_color = 'button_bg_color'
        self.entry_bg_color = 'entry_bg_color'
        self.bg_color = 'bg_color'
        self.font = 'font'
        self.button_size = 'button_size'
        self.name_idx = 'name_idx'
        self.user_email = 'user_email'
        self.email_password_idx = 'email_password_idx'
        self.phone_number = 'phone_number'
        self.upi_id = 'upi_id'
        self.create_new_entry_flag = False
        self.list_of_items_flag = False

    def add_members_to_list(self, box):
        for i in box.curselection():
            if box.get(i) not in self.list_of_members:
                self.list_of_members.append(box.get(i))

    def add_members(self):
        if self.event.get() == '':
            self.add_event_name_error = Label(master=self.main_panel,
                                              text='Please a title for the event',
                                              font=(self.variables[self.font], 10),
                                              bg=self.variables[self.bg_color],
                                              fg='red')
            self.add_event_name_error.pack(padx=4, pady=4, fill='x')
        else:
            add_member_window = Toplevel()
            self.add_member_window = add_member_window
            self.add_member_window.title('Select Members for the Event')
            self.add_member_window.geometry('500x500')
            # Icon of add member window
            icon = PhotoImage(file='images/plus.png')
            self.add_member_window.iconphoto(False, icon)

            scrollbar = Scrollbar(self.add_member_window)
            scrollbar.pack(side=RIGHT, fill=Y)

            label = Label(self.add_member_window,
                          text='Select members below',
                          font=(self.variables[self.font], 12),
                          bg=self.variables[self.bg_color],
                          padx=10, pady=15)
            label.pack()

            list_box = Listbox(self.add_member_window, selectmode="multiple",
                               yscrollcommand=scrollbar.set)
            self.list_box = list_box

            self.list_box.config(font=(self.variables[self.font], 15, 'bold'),
                                 bd=5,
                                 bg=self.variables[self.entry_bg_color])
            self.list_box.pack(padx=10, pady=10, expand=YES, fill="both")

            list_of_members_1 = list(members().keys())

            for each_item in range(len(list_of_members_1)):
                self.list_box.insert(END, list_of_members_1[each_item])
                self.list_box.itemconfig(each_item, bg=self.variables[self.entry_bg_color])

            # Attach listbox to vertical scrollbar
            scrollbar.config(troughcolor=self.variables[self.bg_color], command=self.list_box.yview)

            add_members_window_button_frame = Frame(self.add_member_window,
                                                    bg=self.variables[self.bg_color])
            edit_icon = PhotoImage(file="images/edit.png")
            Button(master=add_members_window_button_frame,
                   bd=0,
                   bg=self.variables[self.bg_color],
                   height=30,
                   width=30,
                   image=edit_icon,
                   command=lambda: [self.edit_user()]).pack(side='left', padx=10, pady=10)
            delete_icon = PhotoImage(file="images/delete-1.png")
            Button(master=add_members_window_button_frame,
                   bd=0,
                   bg=self.variables[self.bg_color],
                   height=30,
                   width=30,
                   image=delete_icon,
                   command=lambda: [self.create_confirmation_window(self.list_box)]).pack(side='left', padx=10, pady=10)
            Button(master=add_members_window_button_frame, bd=1, fg=self.variables[self.fg_color],
                   font=(self.variables[self.font], int(self.variables[self.button_size])),
                   text='Add New Members', bg=self.variables[self.button_bg_color],
                   command=lambda: [self.entry_new_member()]).pack(side='left', padx=10, pady=10)

            Button(master=add_members_window_button_frame,
                   bd=1,
                   fg=self.variables[self.fg_color],
                   font=(self.variables[self.font], int(self.variables[self.button_size])),
                   text='Select Members',
                   bg=self.variables[self.button_bg_color],
                   command=lambda: [self.add_members_to_list(self.list_box),
                                    self.create_d_investor_money(),
                                    self.destory_add_member_window(self.add_member_window),
                                    ]
                   ).pack(side='left', padx=10, pady=10)
            add_members_window_button_frame.pack(side='bottom')

            self.add_member_window.config(bg=self.variables[self.bg_color])
            self.add_member_window.grab_set()
            self.add_member_window.mainloop()

    def destory_add_member_window(self, window):
        if self.create_new_entry_flag:
            self.clicked_user_drop.after(0, self.clicked_user_drop.destroy()),
            self.select_member_label.after(0, self.select_member_label.destroy()),
            self.enter_money_entry.after(0, self.enter_money_entry.destroy()),
            self.reason_label.after(0, self.reason_label.destroy()),
            self.reason_entry.after(0, self.reason_entry.destroy()),
            self.create_new_entry_flag = False

        if not self.list_of_members:
            Label(master=self.add_member_window,
                  text='Please select atleast one member',
                  font=(self.variables[self.font], 10),
                  bg=self.variables[self.bg_color],
                  fg='red').pack(padx=4, pady=4, fill='x')
        else:
            if self.add_event_name_error:
                self.add_event_name_error.after(0, self.add_event_name_error.destroy())
            self.list_of_items(),
            self.create_new_entry()
            window.destroy()
        Button(master=self.first_row_frame,
               bd=1,
               fg=self.variables[self.fg_color],
               font=(self.variables[self.font], int(self.variables[self.button_size])),
               text='Done',
               bg=self.variables[self.button_bg_color],
               command=self.send_emails).grid(padx=50, pady=5, row=0, column=4)

    def create_new_entry(self):
        if not self.create_new_entry_flag:
            self.item = StringVar()
            money_var = IntVar()
            self.money_var = money_var
            self.money_var.set(0)
            clicked_user = StringVar()

            clicked_user.set("Select a Member")
            self.clicked_user_drop = OptionMenu(self.new_entry_frame, clicked_user, *self.list_of_members)
            self.clicked_user_drop.config(font=(self.variables[self.font], 12, 'bold'),
                                          bd=3,
                                          bg=self.variables[self.entry_bg_color], justify='right')
            self.clicked_user_drop.grid(padx=5, pady=5, row=0, column=0)
            self.clicked_user_drop["menu"]["background"] = self.variables[self.entry_bg_color]
            self.clicked_user_drop["menu"]["font"] = (self.variables[self.font], 13, 'bold')
            self.clicked_user_drop["menu"]["activeborderwidth"] = '4'

            self.select_member_label = Label(master=self.new_entry_frame,
                                             text="Paid",
                                             font=(self.variables[self.font], 15, 'bold'),
                                             bg=self.variables[self.bg_color])

            self.select_member_label.grid(padx=5, pady=5, row=0, column=1)
            enter_money_entry = Entry(master=self.new_entry_frame,
                                      font=(self.variables[self.font], 15, 'bold'),
                                      textvariable=self.money_var,
                                      bd=5,
                                      bg=self.variables[self.entry_bg_color],
                                      justify='right')
            self.enter_money_entry = enter_money_entry
            self.enter_money_entry.grid(padx=5, pady=5, row=0, column=2)
            self.reason_label = Label(master=self.new_entry_frame,
                                      text="For",
                                      font=(self.variables[self.font], 15, 'bold'),
                                      bg=self.variables[self.bg_color])
            self.reason_label.grid(padx=5, pady=5, row=0, column=3)
            reason_entry = Entry(master=self.new_entry_frame,
                                 font=(self.variables[self.font], 15, 'bold'),
                                 textvariable=self.item,
                                 bd=5,
                                 bg=self.variables[self.entry_bg_color],
                                 justify='right')
            self.reason_entry = reason_entry
            self.reason_entry.grid(padx=5, pady=5, row=0, column=4)

            def reset_new_entry():
                self.money_var.set(0)
                self.item.set('')
                clicked_user.set("Select a Member")

            Button(self.new_entry_frame,
                   bd=1,
                   fg=self.variables[self.fg_color],
                   font=(self.variables[self.font], int(self.variables[self.button_size]), 'bold'),
                   text='Submit', bg=self.variables[self.button_bg_color],
                   command=lambda: [
                       self.member_input(clicked_user, self.money_var),
                       self.item_to_list(clicked_user, self.item, self.money_var),
                       reset_new_entry(),
                       self.total_money_label.after(0, self.total_money_label.destroy()),
                       self.individual_share_label.after(0, self.individual_share_label.destroy()),
                       self.add_item_to_list()
                   ]).grid(padx=5, pady=5, row=0, column=5)

            self.create_new_entry_flag = True

    def add_item_to_list(self):
        self.item_list.insert(parent='', index='end', text='', values=(len(self.items), *self.items[-1]))

        self.total_money_label = Label(self.extra_details_panel,
                                       text=f"Total Paid Money: {self.total_money.get()}",
                                       font=(self.variables[self.font], 12),
                                       bg=self.variables[self.bg_color])
        self.total_money_label.grid(row=0, column=0, padx=4, pady=4, sticky=S)

        self.individual_share.set(round(self.total_money.get() / len(self.list_of_members), 2))
        self.individual_share_label = Label(self.extra_details_panel,
                                            text=f"Individual Share: {self.individual_share.get()}",
                                            font=(self.variables[self.font], 12),
                                            bg=self.variables[self.bg_color])
        self.individual_share_label.grid(row=1, column=0, padx=4, pady=4, sticky=S)

    def list_of_items(self):
        if not self.list_of_items_flag:
            self.list_of_items_frame = Frame(self.main_panel, bg=self.variables[self.entry_bg_color])
            Label(self.list_of_items_frame,
                  text="List of event's expenses",
                  font=(self.variables[self.font], 12),
                  bg=self.variables[self.entry_bg_color]).pack(side='top', padx=4, pady=4)
            item_list = ttk.Treeview(self.list_of_items_frame)
            self.item_list = item_list
            style = ttk.Style()
            style.configure("Treeview", foreground=self.variables[self.fg_color],
                            background=self.variables[self.bg_color])
            style.configure("Treeview.Heading", background="black", foreground='#00337f', font=8)
            style.configure("Treeview.Heading", borderwidth=8)

            self.item_list['columns'] = ('S.No.', "member's_name", "Paid For", "Paid")

            self.item_list.column("#0", width=0, stretch=NO)
            self.item_list.column('S.No.', anchor=CENTER, width=80)
            self.item_list.column("member's_name", anchor=CENTER, width=80)
            self.item_list.column("Paid For", anchor=CENTER, width=120)
            self.item_list.column("Paid", anchor=CENTER, width=80)

            self.item_list.heading("#0", text="", anchor=CENTER)
            self.item_list.heading('S.No.', text='S.No.', anchor=CENTER)
            self.item_list.heading("member's_name", text='Name', anchor=CENTER)
            self.item_list.heading("Paid For", text='Paid For', anchor=CENTER)
            self.item_list.heading("Paid", text='Money', anchor=CENTER)

            self.item_list.pack(side='top')
            self.list_of_items_frame.pack(padx=50, pady=50, side='left')

            self.extra_details_panel = Frame(self.main_panel, bg=self.variables[self.bg_color])

            self.total_money = DoubleVar()
            self.total_money.set(0.0)
            self.total_money_label = Label(master=self.extra_details_panel,
                                           text=f"Total Paid Money: {self.total_money.get()}",
                                           font=(self.variables[self.font], 12),
                                           bg=self.variables[self.bg_color])
            self.total_money_label.grid(row=0, column=0, padx=4, pady=4, sticky=E)

            self.individual_share = DoubleVar()
            self.individual_share.set(0.0)
            self.individual_share_label = Label(self.extra_details_panel,
                                                text=f"Individual Share: {self.individual_share.get()}",
                                                font=(self.variables[self.font], 12),
                                                bg=self.variables[self.bg_color])
            self.individual_share_label.grid(row=1, column=0, padx=4, pady=4, sticky=E)

            self.extra_details_panel.pack(padx=10, pady=10, side='left')
            self.main_panel.geometry("1050x500")
            self.list_of_items_flag = True

    def update_members_list(self, user_name):
        self.list_box.insert(END, user_name)

    def edit_user(self):
        edit_user_window = Toplevel()
        edit_user_window.title("Edit Member's Details")
        # Icon of the edit member window
        p = PhotoImage(file='images/edit.png')
        edit_user_window.iconphoto(False, p)
        edit_user_window.config(bg=self.variables[self.bg_color])

        users_dict = members()
        selected_user = StringVar()
        selected_user_email = StringVar()
        self.selected_user_email = selected_user_email
        selected_user.set("Select a User")

        # Top Frame
        top_frame = Frame(edit_user_window, bg=self.variables[self.bg_color])
        # bottom frame
        bottom_frame = Frame(edit_user_window, bg=self.variables[self.bg_color])
        self.bottom_frame = bottom_frame
        selected_user_drop = OptionMenu(top_frame, selected_user, *list(users_dict.keys()))
        selected_user_drop.config(font=(self.variables[self.font], 12, 'bold'),
                                  bd=2,
                                  bg=self.variables[self.entry_bg_color],
                                  justify='right')
        selected_user_drop.pack(padx=5, pady=5, side='left')
        selected_user_drop["menu"]["background"] = self.variables[self.entry_bg_color]
        selected_user_drop["menu"]["font"] = (self.variables[self.font], 12, 'bold')
        selected_user_drop["menu"]["activeborderwidth"] = '1'

        Button(top_frame, bd=1, fg=self.variables[self.fg_color],
               font=(self.variables[self.font], int(self.variables[self.button_size]), 'bold'),
               text='Get', bg=self.variables[self.button_bg_color], command=lambda: [
                self.update_entry(users_dict, selected_user)]).pack(padx=5, pady=5, side='left')

        top_frame.pack(side='top')
        self.bottom_frame.pack(side='top')

        button_frame = Frame(edit_user_window, bg=self.variables[self.bg_color])
        Button(master=button_frame,
               bd=1,
               fg=self.variables[self.fg_color],
               font=(self.variables[self.font], int(self.variables[self.button_size]), 'bold'),
               text='Save',
               bg=self.variables[self.button_bg_color],
               command=lambda: [
                   Database.update_email(selected_user.get(), self.selected_user_email.get()),
                   edit_user_window.destroy()]).pack(padx=5, pady=5)
        button_frame.pack(side='bottom')
        edit_user_window.geometry('400x150')
        edit_user_window.grab_set()
        edit_user_window.mainloop()

    def update_entry(self, users_dict, selected_user):
        Label(self.bottom_frame, text="Email", font=(self.variables[self.font], 15, 'bold'),
              bg=self.variables[self.bg_color]).pack(padx=5, pady=5, side='left')
        self.selected_user_email.set(users_dict[selected_user.get()])
        Entry(self.bottom_frame, font=(self.variables[self.font], 12, 'bold'),
              textvariable=self.selected_user_email, bd=5, bg=self.variables[self.entry_bg_color],
              justify='right').pack(padx=5, pady=5, side='left')

    def create_confirmation_window(self, users):
        if [users.get(i) for i in users.curselection()]:
            confirmation_window = Toplevel()
            confirmation_window.title('Delete Members')
            icon = PhotoImage(file='images/delete.png')
            confirmation_window.iconphoto(False, icon)

            Label(master=confirmation_window,
                  text=f"Are you sure, you want to remove '{', '.join([users.get(i) for i in users.curselection()])}'",
                  fg='red',
                  font=(self.variables[self.font], 12, 'bold'),
                  bg=self.variables[self.bg_color]).pack(side='top', padx=5, pady=5, fill='both')
            Button(confirmation_window, bd=1, fg=self.variables[self.fg_color],
                   font=(self.variables[self.font], int(self.variables[self.button_size]), 'bold'),
                   text='Delete', bg=self.variables[self.button_bg_color], command=lambda: [
                    confirmation_window.destroy(),
                    self.delete_user(),
                    self.add_member_window.destroy(),
                    self.add_members()]).pack(padx=5, pady=5, side='top')
            confirmation_window.config(bg=self.variables[self.bg_color])
            confirmation_window.grab_set()
            confirmation_window.mainloop()

    def delete_user(self):
        for i in self.list_box.curselection():
            Database.remove_member(self.list_box.get(i))

    def entry_new_member(self):
        self.new_member_window = Toplevel()
        self.new_member_window.title("Add New Member")
        # Icon of the new member window
        p = PhotoImage(file='images/add_members.png')
        self.new_member_window.iconphoto(False, p)
        # Main panel's background color
        self.new_member_window.config(bg=self.variables[self.bg_color])

        user_name = StringVar()
        email = StringVar()

        top_frame = Frame(self.new_member_window, bg=self.variables[self.bg_color])
        top_frame.pack(side='top')

        # Username Entry
        label_frame = Frame(top_frame, bg=self.variables[self.bg_color])
        label_frame.pack(side='left')

        Label(label_frame, text="Member's Name: ", font=(self.variables[self.font], 15, 'bold'),
              bg=self.variables[self.bg_color]).grid(row=0, column=0, padx=5, pady=5, sticky=E)
        Label(label_frame, text="Email: ", font=(self.variables[self.font], 15, 'bold'),
              bg=self.variables[self.bg_color]).grid(row=1, column=0, padx=5, pady=5, sticky=E)

        # Password entry
        entry_frame = Frame(top_frame, bg=self.variables[self.bg_color])
        entry_frame.pack(side='right')

        Entry(entry_frame, font=(self.variables[self.font], 15, 'bold'), textvariable=user_name, bd=5,
              bg=self.variables[self.entry_bg_color], justify='right') \
            .pack(padx=5, pady=5)
        Entry(entry_frame, font=(self.variables[self.font], 15, 'bold'), textvariable=email, bd=5,
              bg=self.variables[self.entry_bg_color], justify='right') \
            .pack(padx=5, pady=5)

        # Submit button
        button_frame = Frame(self.new_member_window, bg=self.variables[self.bg_color])
        button_frame.pack(side='bottom')
        Button(master=button_frame,
               bd=1,
               fg=self.variables[self.fg_color],
               font=(self.variables[self.font], int(self.variables[self.button_size]), 'bold'),
               text='Submit',
               bg=self.variables[self.button_bg_color],
               command=lambda: [self.insert_new_member(user_name, email)]).pack(padx=5, pady=5)
        self.new_member_window.grab_set()
        self.new_member_window.mainloop()

    def insert_new_member(self, user_name, email):
        if user_name.get() == '' or email.get() == '':
            Label(self.new_member_window,
                  text='Username or email is not valid',
                  font=(self.variables[self.font], 10),
                  bg=self.variables[self.bg_color],
                  fg='red').pack(padx=4, pady=4, side='top', fill='x')
        elif user_name.get() in members().keys():
            Label(self.new_member_window,
                  text='Username is already exits',
                  font=(self.variables[self.font], 10),
                  bg=self.variables[self.bg_color],
                  fg='red').pack(padx=4, pady=4, side='top', fill='x')
        else:
            user_name = user_name.get()
            email = email.get()
            inv = Database(user_name, email)
            Database.insert_member(inv)

            self.members_email[user_name] = email
            self.update_members_list(user_name)
            self.new_member_window.destroy()

    def create_d_investor_money(self):
        for member in self.list_of_members:
            if member not in self.d_investor_money.keys():
                self.d_investor_money[member] = 0

    def member_input(self, username, money_var):
        member = username.get()
        money = money_var.get()
        self.total_money.set(self.total_money.get() + money)
        self.d_investor_money[member] += money

    def create_profile_window(self):
        profile_window = Toplevel()
        profile_window.title('Profile')
        profile_window.config(bg=self.variables[self.bg_color])
        # Icon of the main window
        p = PhotoImage(file='images/profile.png')
        profile_window.iconphoto(False, p)

        name_var = StringVar()
        name_var.set(self.variables[self.name_idx])
        email_var = StringVar()
        email_var.set(self.variables[self.user_email])
        email_password_var = StringVar()
        email_password_var.set(self.variables[self.email_password_idx])
        phone_number_var = StringVar()
        phone_number_var.set(self.variables[self.phone_number])
        upi_id_var = StringVar()
        upi_id_var.set(self.variables[self.upi_id])

        Label(profile_window, text='Please add your personal information before using the app',
              font=(self.variables[self.font], 12, 'bold'), fg='#69696E',
              bg=self.variables[self.bg_color]).grid(row=0, column=0, columnspan=3, padx=8, pady=4)

        Label(profile_window, text='Name', font=(self.variables[self.font], 12, 'bold'),
              bg=self.variables[self.bg_color]).grid(row=1, column=0, padx=4, pady=4, sticky=E)

        Entry(profile_window, font=(self.variables[self.font], 12, 'bold'), textvariable=name_var, bd=5,
              bg=self.variables[self.entry_bg_color], justify='right').grid(row=1, column=1, padx=4, pady=4)

        Label(profile_window, text='Email', font=(self.variables[self.font], 12, 'bold'),
              bg=self.variables[self.bg_color]).grid(row=2, column=0, padx=4, pady=4, sticky=E)

        Entry(profile_window, font=(self.variables[self.font], 12, 'bold'), textvariable=email_var, bd=5,
              bg=self.variables[self.entry_bg_color], justify='right').grid(row=2, column=1, padx=4, pady=4)

        Label(profile_window, text='Phone No.', font=(self.variables[self.font], 12, 'bold'),
              bg=self.variables[self.bg_color]).grid(row=3, column=0, padx=4, pady=4, sticky=E)

        Entry(profile_window, font=(self.variables[self.font], 12, 'bold'), textvariable=phone_number_var, bd=5,
              bg=self.variables[self.entry_bg_color], justify='right').grid(row=3, column=1, padx=4, pady=4)

        Label(profile_window, text='UPI IDs', font=(self.variables[self.font], 12, 'bold'),
              bg=self.variables[self.bg_color]).grid(row=4, column=0, padx=4, pady=4, sticky=E)

        Entry(profile_window, font=(self.variables[self.font], 12, 'bold'), textvariable=upi_id_var, bd=5,
              bg=self.variables[self.entry_bg_color], justify='right').grid(row=4, column=1, padx=4, pady=4)

        Label(profile_window, text='App Password', font=(self.variables[self.font], 12, 'bold'),
              bg=self.variables[self.bg_color]).grid(row=5, column=0, padx=4, pady=4, sticky=E)

        Entry(profile_window, font=(self.variables[self.font], 12, 'bold'), textvariable=email_password_var, bd=5,
              bg=self.variables[self.entry_bg_color], justify='right').grid(row=5, column=1, padx=4, pady=4)

        link_label = Label(profile_window, text='Follow this link to setup your app password',
                           font=(self.variables[self.font], 10, 'bold'), fg='blue',
                           bg=self.variables[self.bg_color], cursor="hand2")
        link_label.grid(row=6, column=0, columnspan=3, padx=8, pady=4)
        link_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://myaccount.google.com/apppasswords"))

        Label(profile_window, text='QR Codes', font=(self.variables[self.font], 12, 'bold'),
              bg=self.variables[self.bg_color]).grid(row=7, column=0, padx=4, pady=4, sticky=E)

        Button(master=profile_window,
               bd=1,
               fg=self.variables[self.fg_color],
               font=(self.variables[self.font], int(self.variables[self.button_size])),
               height=1,
               width=22,
               text='Browse Files',
               bg=self.variables[self.button_bg_color],
               command=lambda: [browse_files()]
               ).grid(row=7, column=1, padx=4, pady=4)

        Button(master=profile_window,
               bd=1,
               fg=self.variables[self.fg_color],
               font=(self.variables[self.font], int(self.variables[self.button_size])),
               height=1,
               width=10,
               text='Save',
               bg=self.variables[self.button_bg_color],
               command=lambda: [save_profile({self.name_idx: name_var,
                                              self.user_email: email_var,
                                              self.phone_number: phone_number_var,
                                              self.upi_id: upi_id_var,
                                              self.email_password_idx: email_password_var
                                              }),
                                restart_application(self.main_panel)]
               ).grid(row=8, column=0, columnspan=3, padx=4, pady=30)

        profile_window.geometry("530x400")
        profile_window.grab_set()
        profile_window.mainloop()

    def create_restart_dialog_window(self):
        restart_dialog_window = Toplevel()
        restart_dialog_window.title('Settings')
        p = PhotoImage(file='images/settings.png')
        restart_dialog_window.iconphoto(False, p)
        restart_dialog_window.config(bg=self.variables[self.bg_color])

        Label(restart_dialog_window, text='In order to apply the changes, the Application must be restarted',
              font=(self.variables[self.font], 10, 'bold'), fg='red',
              bg=self.variables[self.bg_color]). \
            pack(padx=4, pady=4)

        button_frame = Frame(restart_dialog_window, bg=self.variables[self.bg_color])

        Button(button_frame, bd=1, fg=self.variables[self.fg_color], font=(
            self.variables[self.font], int(self.variables[self.button_size])), text='Restart',
               bg=self.variables[self.button_bg_color], command=lambda: [restart_application(self.main_panel)]). \
            pack(side='left', padx=4, pady=4)

        def destory_restart_dialog_window():
            restart_dialog_window.destroy()

        Button(button_frame, bd=1, fg=self.variables[self.fg_color], font=(
            self.variables[self.font], int(self.variables[self.button_size])), text='Cancel',
               bg=self.variables[self.button_bg_color], command=lambda: [destory_restart_dialog_window()]). \
            pack(side='left', padx=4, pady=4)
        button_frame.pack(side='bottom')

        restart_dialog_window.grab_set()
        restart_dialog_window.mainloop()

    def create_setting_window(self):
        setting_window = Toplevel()
        setting_window.title('Settings')
        # Icon of the main window
        p = PhotoImage(file='images/settings.png')
        setting_window.iconphoto(False, p)

        setting_option_frame = Frame(setting_window, bg=self.variables[self.bg_color])

        Label(setting_option_frame, text="Button's Foreground Color",
              font=(self.variables[self.font], 15, 'bold'),
              bg=self.variables[self.bg_color]).grid(row=0, column=0, padx=25, pady=4, sticky=E)
        Button(
            master=setting_option_frame,
            bd=1,
            fg=self.variables[self.fg_color],
            font=(self.variables[self.font], int(self.variables[self.button_size])),
            text='Pick Color',
            bg=self.variables[self.fg_color],
            command=lambda: [change_value(self.fg_color)]
        ).grid(row=0, column=1, padx=4, pady=4)

        Label(setting_option_frame, text="Button's Background Color",
              font=(self.variables[self.font], 15, 'bold'),
              bg=self.variables[self.bg_color]).grid(row=1, column=0, padx=25, pady=4, sticky=E)
        Button(
            master=setting_option_frame,
            bd=1,
            fg=self.variables[self.fg_color],
            font=(self.variables[self.font], int(self.variables[self.button_size])),
            text='Pick Color',
            bg=self.variables[self.button_bg_color],
            command=lambda: [change_value(self.button_bg_color)]
        ).grid(row=1, column=1, padx=4, pady=4)

        Label(setting_option_frame, text="Entry's Background Color",
              font=(self.variables[self.font], 15, 'bold'),
              bg=self.variables[self.bg_color]).grid(row=2, column=0, padx=25, pady=4, sticky=E)
        Button(setting_option_frame, bd=1, fg=self.variables[self.fg_color], font=(
            self.variables[self.font], int(self.variables[self.button_size])), text='Pick Color',
               bg=self.variables[self.entry_bg_color],
               command=lambda: [change_value(self.entry_bg_color)]). \
            grid(row=2, column=1, padx=4, pady=4)

        Label(setting_option_frame, text="Window's Background Color",
              font=(self.variables[self.font], 15, 'bold'),
              bg=self.variables[self.bg_color]).grid(row=3, column=0, padx=25, pady=4, sticky=E)
        Button(setting_option_frame, bd=1, fg=self.variables[self.fg_color], font=(
            self.variables[self.font], int(self.variables[self.button_size])), text='Pick Color',
               bg=self.variables[self.bg_color], command=lambda: [change_value(self.bg_color)]). \
            grid(row=3, column=1, padx=4, pady=4)

        Label(setting_option_frame, text="Font", font=(self.variables[self.font], 15, 'bold'),
              bg=self.variables[self.bg_color]).grid(row=4, column=0, padx=25, pady=4, sticky=E)

        button_font_value = StringVar()
        button_font_value.set(self.variables[self.font])
        button_font_drop = OptionMenu(setting_option_frame, button_font_value, *font_list.families())
        button_font_drop.config(
            font=(self.variables[self.font], int(self.variables[self.button_size])),
            bd=2, bg=self.variables[self.button_bg_color])
        button_font_drop.grid(padx=5, pady=5, row=4, column=1)
        button_font_drop["menu"]["background"] = self.variables[self.bg_color]
        for x in range(0, int(button_font_drop['menu'].index('end'))):
            button_font_drop['menu'].entryconfig(x, font=font_list.Font(family=font_list.families()[x]))
        button_font_drop["menu"]["activeborderwidth"] = '2'

        setting_option_frame.pack(side='top', fill='both', expand=True)

        Button(setting_window, bd=1, fg=self.variables[self.fg_color], font=(
            self.variables[self.font], int(self.variables[self.button_size])), text='Save Changes',
               bg=self.variables[self.button_bg_color], command=lambda: [
                change_font(self.font, button_font_value), self.create_restart_dialog_window()]). \
            pack(side='bottom', padx=4, pady=20)

        # setting_window window's background color
        setting_window.config(bg=self.variables[self.bg_color])
        setting_window.geometry("800x400")
        setting_window.grab_set()
        setting_window.mainloop()

    def item_to_csv(self, list_name):
        users = []
        item_names = []
        items_money = []
        for user, item, mon in self.items:
            users.append(user)
            item_names.append(item)
            items_money.append(mon)
        for member in self.list_of_members:
            if member not in users:
                users.append(member)
                item_names.append('--')
                items_money.append(0)

        if not os.path.exists(os.path.join(app_data_location, 'items')):
            os.mkdir(os.path.join(app_data_location, 'items'))
        with open(os.path.join(app_data_location, 'items', list_name), 'w') as out:
            out.write('S.No.,Paid By,Item Names,Item Money\n')
            for j in range(len(item_names)):
                out.write(str(j + 1) + ',' + users[j] + ',' + item_names[j] + ',' + str(items_money[j]) + '\n')

    def item_to_list(self, name, item, mon):
        user = name.get()
        item_msg = item.get()
        mon_msg = mon.get()
        if item_msg == '':
            self.items.append((user, 'Not Mentioned', mon_msg))
        else:
            self.items.append((user, item_msg, mon_msg))

    def send_emails(self):
        name = self.variables[self.name_idx]
        my_email_address = self.variables[self.user_email]
        email_password = self.variables[self.email_password_idx]

        share = self.total_money.get() / len(self.d_investor_money)
        p4 = ''
        phone = self.variables[self.phone_number]
        phone_pay_upi, g_pay_upi, paytm_upi = get_upi_ids(self.variables[self.upi_id])

        event_name = self.event.get()
        csv_name = item_name(event_name)
        self.item_to_csv(csv_name)

        for mem in self.d_investor_money:
            if mem != name:
                msg = MIMEMultipart()
                msg['Subject'] = f"Your share to pay in {event_name}"
                msg['From'] = my_email_address
                msg['To'] = self.members_email[mem]

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

                if share - self.d_investor_money[mem] > 0:
                    try:
                        qr_code_line_1 = """<p style="margin: 0; font-size: 14px;"><em><strong>QR Codes are given below
                         to make payments</strong></em></p>"""
                        qr_code_line_2 = """<div align="center" style="line-height:10px"><img src="cid:qrcode"
                         style="display: block; height: auto; border: 0; width: 325px; max-width: 100%;" width="325"/>
                         </div>"""
                        qr_code = MIMEImage(open('./images/QR_Codes.png', 'rb').read())
                        qr_code.add_header('Content-ID', '<qrcode>')
                        msg.attach(qr_code)
                        pay_message = open('messages/pay_money_message.html') \
                            .read().format(v1=self.total_money.get(),
                                           v2=round(share, 2),
                                           v3=self.d_investor_money[mem],
                                           v4=round(share - self.d_investor_money[mem], 2),
                                           v5=name,
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
                                           v4=round(share - self.d_investor_money[mem], 2),
                                           v5=name,
                                           phone=phone,
                                           phone_pay_upi=phone_pay_upi,
                                           g_pay_upi=g_pay_upi,
                                           paytm_upi=paytm_upi,
                                           qr_code_line_1="",
                                           qr_code_line_2="")
                        msg_body = MIMEText(pay_message, 'html')

                    p4 += f'<br/>{mem} will give you {round(share - self.d_investor_money[mem], 2)}&#8377;'
                else:
                    receive_money_message = open('messages/receive_money_message.html') \
                        .read().format(v1=self.total_money.get(),
                                       v2=round(share, 2),
                                       v3=self.d_investor_money[mem],
                                       v4=name,
                                       v5=round(self.d_investor_money[mem] - share, 2))

                    msg_body = MIMEText(receive_money_message, 'html')

                    p4 += f'<br/>You have to give {round(self.d_investor_money[mem] - share, 2)}&#8377; to {mem}'

                logo = MIMEImage(open('./images/logo.png', 'rb').read())
                logo.add_header('Content-ID', '<logo>')
                msg.attach(logo)

                msg.attach(msg_body)

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(my_email_address, email_password)
                    smtp.send_message(msg)

        d_msg = MIMEMultipart()
        d_msg['Subject'] = f"Share in {event_name}"
        d_msg['From'] = my_email_address
        d_msg['To'] = my_email_address
        d_msg.attach(attachment)
        receive_email = open('messages/receive_email.html') \
            .read().format(p1=self.total_money.get(),
                           p2=round(share, 2),
                           p3=self.d_investor_money[name],
                           p4=p4)
        d_msg_body = MIMEText(receive_email, 'html')
        logo = MIMEImage(open('./images/logo.png', 'rb').read())
        logo.add_header('Content-ID', '<logo>')
        d_msg.attach(logo)

        d_msg.attach(d_msg_body)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(my_email_address, email_password)
            smtp.send_message(d_msg)

        notification.notify(title="Share App", message="Mails sent", app_name="Share App", app_icon='./images/logo.ico')

        self.after_sending_emails()

    def after_sending_emails(self):
        done_window = Toplevel()
        done_window.config(bg=self.variables[self.bg_color])
        done_window.title('Done')
        p = PhotoImage(file='images/done.png')
        done_window.iconphoto(False, p)

        first_frame = Frame(done_window, bg=self.variables[self.bg_color])
        Label(master=first_frame,
              image=p,
              font=(self.variables[self.font], self.variables[self.button_size], 'bold'),
              fg=self.variables[self.fg_color],
              bg=self.variables[self.bg_color]).grid(row=0, column=0, padx=10, pady=10)
        Label(master=first_frame,
              text='Emails are sent to members with their share and payment details',
              font=(self.variables[self.font], self.variables[self.button_size], 'bold'),
              fg=self.variables[self.fg_color],
              bg=self.variables[self.bg_color]).grid(row=0, column=1, padx=10, pady=10)
        first_frame.pack(side='top', fill='x', expand=True)

        second_frame = Frame(done_window, bg=self.variables[self.bg_color])
        Button(master=second_frame,
               bd=1,
               fg=self.variables[self.fg_color],
               width=15,
               font=(self.variables[self.font], int(self.variables[self.button_size])),
               text='Fill a new one',
               bg=self.variables[self.button_bg_color],
               command=lambda: [restart_application(self.main_panel)]) \
            .grid(row=0, column=0, padx=10, pady=20, sticky="nsew")
        Button(master=second_frame,
               bd=1,
               fg=self.variables[self.fg_color],
               width=15,
               font=(self.variables[self.font], int(self.variables[self.button_size])),
               text='Close',
               bg=self.variables[self.button_bg_color],
               command=lambda: [self.main_panel.destroy(), conn.close()]). \
            grid(row=0, column=1, padx=10, pady=20, sticky="nsew")
        second_frame.pack(side='top')

        done_window.grab_set()
        done_window.mainloop()

    def run(self):
        self.members_email = members()
        self.list_of_members = []
        self.items = []
        self.variables = get_variable_values()

        # Creating main window
        self.main_panel = Tk()
        self.main_panel.title("Share App")

        # Icon of the main window
        self.main_panel.iconbitmap('images/logo.ico')

        # Creating Menubar
        menu_bar = Menu(self.main_panel)

        # File menu
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Settings", menu=file_menu)

        file_menu.add_command(label='Profile', command=self.create_profile_window)
        file_menu.add_command(label='Settings', command=self.create_setting_window)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=lambda: [self.main_panel.destroy()])

        # Main panel's background color
        self.main_panel.config(bg=self.variables[self.bg_color], menu=menu_bar)

        if self.variables[self.name_idx] == '' or \
                self.variables[self.user_email] == '' or \
                self.variables[self.email_password_idx] == '':
            Label(master=self.main_panel,
                  text='You have to add your profile details to use the app',
                  font=(self.variables[self.font], self.variables[self.button_size], 'bold'),
                  fg='red',
                  bg=self.variables[self.bg_color]).pack(side='top', padx=10, pady=25)
            Button(master=self.first_row_frame,
                   bd=1,
                   fg=self.variables[self.fg_color],
                   width=15,
                   font=(self.variables[self.font], int(self.variables[self.button_size])),
                   text='Setup Profile',
                   bg=self.variables[self.button_bg_color],
                   command=lambda: [self.create_profile_window()]).pack(side='top', padx=10, pady=10)
        else:
            self.event = StringVar()

            # First Row
            first_row_frame = Frame(self.main_panel, bg=self.variables[self.bg_color])
            self.first_row_frame = first_row_frame
            Label(self.first_row_frame, text="Event's Name: ",
                  font=(self.variables[self.font], 15, 'bold'),
                  bg=self.variables[self.bg_color]).grid(padx=4, pady=20, row=0, column=0)
            Entry(
                master=self.first_row_frame,
                font=(self.variables[self.font], 15, 'bold'),
                textvariable=self.event,
                bd=5,
                bg=self.variables[self.entry_bg_color],
                justify='right'
            ).grid(row=0, column=1, padx=4, pady=20)
            Button(self.first_row_frame, bd=1, fg=self.variables[self.fg_color], width=15,
                   font=(self.variables[self.font], int(self.variables[self.button_size])),
                   text='Add Members', bg=self.variables[self.button_bg_color],
                   command=lambda: [self.add_members()]). \
                grid(padx=20, pady=20, row=0, column=2)
            self.first_row_frame.pack(side='top')

            # Second Row (Entry Frame)
            new_entry_frame = Frame(self.main_panel, bg=self.variables[self.bg_color])
            self.new_entry_frame = new_entry_frame
            self.new_entry_frame.pack(side='top')

        # Size of the main panel
        self.main_panel.geometry("1050x200")
        self.main_panel.mainloop()


def restart_application(window):
    window.destroy()
    new_instance = App()
    new_instance.run()


if __name__ == '__main__':
    instance = App()
    instance.run()
