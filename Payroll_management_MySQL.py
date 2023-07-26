from tkinter import *
from tkinter import ttk
import random
import tkinter.messagebox
import datetime
import time
import tkinter as tkr
import tkinter.ttk as tkrtk
import pymysql


class Payroll:

    def __init__(self,root):
        self.root = root
        self.root.title("MySQL Payroll Management System")
        self.root.geometry("1350x800+0+0")

        notebook = ttk.Notebook(self.root)
        self.Tabcontrol1 = ttk.Frame(notebook)
        self.Tabcontrol2 = ttk.Frame(notebook)
        self.Tabcontrol3 = ttk.Frame(notebook)
        notebook.add(self.Tabcontrol1, text='Payroll System')
        notebook.add(self.Tabcontrol2, text='View Payroll')
        notebook.add(self.Tabcontrol3, text='Note Book')
        notebook.grid()

        EmployeeName = StringVar()
        Address = StringVar()
        Reference = StringVar()
        EmployerName = StringVar()
        CityWeighting = StringVar()
        BasicSalary = StringVar()
        OverTime = StringVar()
        OtherPaymentDue = StringVar()
        GrossPay = StringVar()
        Tax = StringVar()
        Pension = StringVar()
        StudentLoan = StringVar()
        NIPayment = StringVar()
        Deductions = StringVar()
        PostCode = StringVar()
        Gender = StringVar()
        Payday = StringVar()
        TaxPeriod = StringVar()
        TaxCode = StringVar()
        NINumber = StringVar()
        NICode = StringVar()
        TaxablePay = StringVar()
        PensionablePay = StringVar()
        NetPay = StringVar()

        text_Input = StringVar()
        global operator
        operator = ""
        CityWeighting.set("")
        BasicSalary.set("")

        # ======================================Calculating function========================================
        def btnClick(numbers):
            global operator
            operator = operator + str(numbers)
            text_Input.set(operator)

        def btnClear():
            global operator
            operator = ""
            text_Input.set("")

        def btnEquals():
            global operator
            sumup = str(eval(operator))
            text_Input.set(sumup)
            operator = ""

        # ======================================Exit function========================================
        def iExit():
            iExit = tkinter.messagebox.askyesno("Payroll System", "Confirm if you want to exit")
            if iExit > 0:
                root.destroy()
                return
        # ======================================Reset function=======================================
        def Reset():
            EmployeeName.set("")
            Address.set("")
            Reference.set("")
            EmployerName.set("")
            CityWeighting.set("")
            BasicSalary.set("")
            OverTime.set("")
            OtherPaymentDue.set("")
            GrossPay.set("")
            Tax.set("")
            Pension.set("")
            StudentLoan.set("")
            NIPayment.set("")
            Deductions.set("")
            PostCode.set("")
            Gender.set("")
            Payday.set("")
            TaxPeriod.set("")
            TaxCode.set("")
            NINumber.set("")
            NICode.set("")
            TaxablePay.set("")
            PensionablePay.set("")
            NetPay.set("")

        # ======================================Pay Function================================================
        def PayRef():
            Payday.set(time.strftime("%d/%m/%y"))
            Refpay = random.randint(15000, 909878)
            Refpaid = ("PR" + str(Refpay))
            Reference.set(Refpaid)

            NIpay = random.randint(32000, 578278)
            NIpaid = ("NI" + str(NIpay))
            NINumber.set(NIpaid)

            iDate = datetime.datetime.now()
            TaxPeriod.set(iDate.month)

            NCode = random.randint(1435, 35765)
            CodeNI = ("NICode" + str(NCode))
            NICode.set(CodeNI)

            iTaxCode = random.randint(5783, 28278)
            PaymentTaxCode = ("TCode" + str(iTaxCode))
            TaxCode.set(PaymentTaxCode)

        def Payment_Function():
            PayRef()

            BS = float(BasicSalary.get())
            CW = float(CityWeighting.get())
            OT = float(OverTime.get())

            MTax = (BS + CW + OT)
            TTax = str('$%.2f'%(MTax))
            Tax.set(TTax)

            M_Pension = ((BS + CW + OT)*0.02)
            MM_Pension = str('$%.2f'%(M_Pension))
            Pension.set(MM_Pension)

            M_StudentLoan = ((BS + CW + OT) * 0.012)
            MM_StudentLoan = str('$%.2f'%(M_StudentLoan))
            StudentLoan.set(MM_StudentLoan)

            M_NIPayment = ((BS + CW + OT) * 0.011)
            MM_NIPayment = str('$%.2f'%(M_NIPayment))
            NIPayment.set(MM_NIPayment)

            Deduct = (MTax + M_Pension + M_StudentLoan + M_NIPayment)
            Deduct_Payment = str('$%.2f'%(Deduct))
            Deductions.set(Deduct_Payment)
            Gross_Pay = str('$%.2f'%(BS + CW + OT))
            GrossPay.set(Gross_Pay)

            NetPayAfter = (BS + CW + OT) + Deduct
            NetAfter = str('$%.2f'%(NetPayAfter))
            NetPay.set(NetAfter)

            TaxablePay.set(TTax)
            PensionablePay.set(MM_Pension)
            OtherPaymentDue.set("0.00")

        # ======================================Add database Function=======================================
        def addData():
            if EmployeeName.get() == "" or Address.get() =="" or Reference.get() == "" :
                tkinter.messagebox.showerror("Enter correct member details")
            else:
                sqlCon = pymysql.connect(host="localhost", user="root", password="", database="payment")
                cur = sqlCon.cursor()
                cur.execute("insert into payment.payment values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)", (
                Reference.get(),
                EmployeeName.get(),
                Address.get(),
                CityWeighting.get(),
                BasicSalary.get(),
                OverTime.get(),
                GrossPay.get(),
                Tax.get(),
                Pension.get(),
                NIPayment.get(),
                Deductions.get(),
                PostCode.get(),
                Gender.get(),
                Payday.get(),
                TaxPeriod.get(),
                TaxCode.get(),
                NINumber.get(),
                NetPay.get(),
                ))

                sqlCon.commit()
                DisplayData()
                sqlCon.close()
                tkinter.messagebox.showinfo("Data entry form", "Record entered successfully")

        # ======================================Display Data function=======================================
        def DisplayData():
            sqlCon = pymysql.connect(host="localhost", user="root", password="", database="payment")
            cur = sqlCon.cursor()
            cur.execute("SELECT * FROM payment.payment")
            result = cur.fetchall()
            if len(result) != 0:
                self.payroll_records.delete(*self.payroll_records.get_children())
                for row in result:
                    self.payroll_records.insert('', END, value=row)
                sqlCon.commit()
            sqlCon.close()

        def WagesInfo(ev):
            viewInfo = self.payroll_records.focus()
            learnerData = self.payroll_records.item(viewInfo)
            row = learnerData["value"]

            Reference.set(row[0])
            EmployeeName.set(row[1])
            Address.set(row[2])
            CityWeighting.set(row[3])
            BasicSalary.set(row[4])
            OverTime.set(row[5])
            GrossPay.set(row[6])
            Tax.set(row[7])
            Pension.set(row[8])
            NIPayment.set(row[9])
            Deductions.set(row[10])
            PostCode.set(row[11])
            Gender.set(row[12])
            Payday.set(row[13])
            TaxPeriod.set(row[14])
            TaxCode.set(row[15])
            NINumber.set(row[16])
            NetPay.set(row[17])

        # ======================================Update Data function=======================================
        def update():
            sqlCon = pymysql.connect(host="localhost", user="root", password="", database="payment")
            cur = sqlCon.cursor()
            cur.execute("UPDATE payment.payment SET firstname=%s, address=%s, cityweighting=%s, basicsalary=%s, overtime=%s, grosspay=%s, tax=%s, pension=%s, nipayment=%s, deductions=%s, postcode=%s, gender=%s, payday=%s, taxperiod=%s, taxcode=%s, ninumber=%s,netpay=%s WHERE ref=%s", (
                Reference.get(),
                EmployeeName.get(),
                Address.get(),
                CityWeighting.get(),
                BasicSalary.get(),
                OverTime.get(),
                GrossPay.get(),
                Tax.get(),
                Pension.get(),
                NIPayment.get(),
                Deductions.get(),
                PostCode.get(),
                Gender.get(),
                Payday.get(),
                TaxPeriod.get(),
                TaxCode.get(),
                NINumber.get(),
                NetPay.get(),
            ))
            sqlCon.commit()
            DisplayData()
            sqlCon.close()
            tkinter.messagebox.showinfo("Data entry form", "Record entered successfully")

        # ======================================Delete Data function=======================================
        def deleteDB():
            sqlCon = pymysql.connect(host="localhost", user="root", password="", database="payment")
            cur = sqlCon.cursor()
            cur.execute("DELETE FROM payment.payment WHERE ref=%s", StudentID.get())

            sqlCon.commit()
            DisplayData()
            sqlCon.close()
            tkinter.messagebox.showinfo("Data entry form", "Record entered successfully")
            Reset()
        # ======================================Frame=======================================================
        MainFrame = Frame(self.Tabcontrol1, bd=10, width=1350, height=700, relief=RIDGE)
        MainFrame.grid()

        Tab2Frame = Frame(self.Tabcontrol2, bd=10, width=1350, height=700, relief=RIDGE)
        Tab2Frame.grid()

        Tab3Frame = Frame(self.Tabcontrol3, bd=10, width=1350, height=700, relief=RIDGE)
        Tab3Frame.grid()

        TopFrame1 = Frame(MainFrame, bd=10, width=1340, height=100,relief=RIDGE)
        TopFrame1.grid()
        TopFrame2 = Frame(MainFrame, bd=10, width=1340, height=100, relief=RIDGE)
        TopFrame2.grid()
        TopFrame3 = Frame(MainFrame, bd=10, width=1340, height=500, relief=RIDGE)
        TopFrame3.grid()

        LeftFrame = Frame(TopFrame3, bd=5, width=1340, height=400, padx=2, bg="cadetblue", relief=RIDGE)
        LeftFrame.pack(side=RIGHT)
        LeftFrame1 = Frame(LeftFrame, bd=5, width=600, height=180, padx=2, relief=RIDGE)
        LeftFrame1.pack(side=TOP)

        LeftFrame2 = Frame(LeftFrame, bd=5, width=600, height=180, padx=2, bg="cadetblue", relief=RIDGE)
        LeftFrame2.pack(side=TOP)
        LeftFrame2Left = Frame(LeftFrame2, bd=5, width=300, height=170, padx=2, relief=RIDGE)
        LeftFrame2Left.pack(side=LEFT)
        LeftFrame2Right = Frame(LeftFrame2, bd=5, width=300, height=170, padx=2, relief=RIDGE)
        LeftFrame2Right.pack(side=RIGHT)

        LeftFrame3Left = Frame(LeftFrame, bd=5, width=320, height=50, padx=2, bg="cadetblue", relief=RIDGE)
        LeftFrame3Left.pack(side=LEFT)
        LeftFrame3Right = Frame(LeftFrame, bd=5, width=320, height=50, padx=2, bg="cadetblue", relief=RIDGE)
        LeftFrame3Right.pack(side=RIGHT)

        RightFrame1 = Frame(TopFrame3, bd=5, width=320,height=400, padx=2, bg="cadetblue", relief=RIDGE)
        RightFrame1.pack(side=RIGHT)
        RightFrame1a = Frame(RightFrame1, bd=5, width=310, height=300, padx=2, relief=RIDGE)
        RightFrame1a.pack(side=TOP)
        RightFrame1b = Frame(RightFrame1, bd=5, width=320, height=100, padx=2, relief=RIDGE)
        RightFrame1b.pack(side=TOP)

        RightFrame2 = Frame(TopFrame3, bd =5, width=300, height=400, padx=2, bg="cadetblue", relief=RIDGE)
        RightFrame2.pack(side=LEFT)
        RightFrame2a = Frame(RightFrame2, bd=5, width=280, height=50, padx=2, relief=RIDGE)
        RightFrame2a.pack(side=TOP)
        RightFrame2b = Frame(RightFrame2, bd=5, width=280, height=180, padx=2, relief=RIDGE)
        RightFrame2b.pack(side=TOP)
        RightFrame2c = Frame(RightFrame2, bd=5, width=280, height=100, padx=2, relief=RIDGE)
        RightFrame2c.pack(side=TOP)
        RightFrame2d = Frame(RightFrame2, bd=5, width=280, height=50, padx=2, relief=RIDGE)
        RightFrame2d.pack(side=TOP)

        #======================================Title========================================================
        self.lblTitle = Label(TopFrame1, font=('arial', 40, 'bold'), text="\tPayroll Management System\t", justify=CENTER)
        self.lblTitle.grid(padx=76)

        # ==================================================================================================
        self.lblEmployeeName = Label(TopFrame2, font=('arial', 12, 'bold'), text="\tEmployee Name\t", bd=5)
        self.lblEmployeeName.grid(row=0, column=0, sticky=W)
        self.txtEmployeeName = Entry(TopFrame2, font=('arial', 12, 'bold'), bd=5, width=57, justify='left', textvariable=EmployeeName)
        self.txtEmployeeName.grid(row=0, column=1)

        self.lblAddress = Label(TopFrame2, font=('arial', 12, 'bold'), text="\tAddress\t", bd=5)
        self.lblAddress.grid(row=1, column=0, sticky=W)
        self.txtAddress = Entry(TopFrame2, font=('arial', 12, 'bold'), bd=5, width=57, justify='left',
                                     textvariable=Address)
        self.txtAddress.grid(row=1, column=1)

        self.lblPostCode = Label(TopFrame2, font=('arial', 12, 'bold'), text="\tPost Code\t", bd=5)
        self.lblPostCode.grid(row=0, column=2, sticky=W)
        self.txtPostCode = Entry(TopFrame2, font=('arial', 12, 'bold'), bd=5, width=57, justify='left',
                                textvariable=PostCode)
        self.txtPostCode.grid(row=0, column=3)

        self.lblGender = Label(TopFrame2, font=('arial', 12, 'bold'), text="\tGender\t", bd=5)
        self.lblGender.grid(row=1, column=2, sticky=W)
        self.cboGender = ttk.Combobox(TopFrame2, textvariable=Gender, state='readonly', font=('arial', 14, 'bold'), width=45)
        self.cboGender['value']=('', 'Female', 'Male')
        self.cboGender.current(0)
        self.cboGender.grid(row=1, column=3)

        #======================================================================================================================
        self.lblPayday = Label(RightFrame2a, font=('arial', 12, 'bold'), text="\tPayday\t", bd=10)
        self.lblPayday.grid(row=0, column=0, sticky=W)
        self.txtPayday = Entry(RightFrame2a, font=('arial', 12, 'bold'), bd=5, width=20, justify='left',
                                textvariable=Payday, state=DISABLED)
        self.txtPayday.grid(row=0, column=1)

        self.lblTaxPeriod = Label(RightFrame2b, font=('arial', 12, 'bold'), text="\tTax Period\t", bd=5)
        self.lblTaxPeriod.grid(row=0, column=0, sticky=W)
        self.txtTaxPeriod = Entry(RightFrame2b, font=('arial', 12, 'bold'), bd=5, width=13, justify='left',
                               textvariable=TaxPeriod, state=DISABLED)
        self.txtTaxPeriod.grid(row=0, column=1)

        self.lblTaxCode = Label(RightFrame2b, font=('arial', 12, 'bold'), text="\tTax Code\t", bd=5)
        self.lblTaxCode.grid(row=1, column=0, sticky=W)
        self.txtTaxCode = Entry(RightFrame2b, font=('arial', 12, 'bold'), bd=5, width=13, justify='left',
                                  textvariable=TaxCode, state=DISABLED)
        self.txtTaxCode.grid(row=1, column=1)

        self.lblNINumber = Label(RightFrame2b, font=('arial', 12, 'bold'), text="\tNI Number\t", bd=5)
        self.lblNINumber.grid(row=2, column=0, sticky=W)
        self.txtNINumber = Entry(RightFrame2b, font=('arial', 12, 'bold'), bd=5, width=13, justify='left',
                                textvariable=NINumber, state=DISABLED)
        self.txtNINumber.grid(row=2, column=1)

        self.lblNICode = Label(RightFrame2b, font=('arial', 12, 'bold'), text="\tNI Code\t", bd=5)
        self.lblNICode.grid(row=3, column=0, sticky=W)
        self.txtNICode = Entry(RightFrame2b, font=('arial', 12, 'bold'), bd=5, width=13, justify='left',
                                 textvariable=NICode, state=DISABLED)
        self.txtNICode.grid(row=3, column=1)

        self.lblNICode = Label(RightFrame2b, font=('arial', 12, 'bold'), text="\tNI Code\t", bd=5)
        self.lblNICode.grid(row=3, column=0, sticky=W)
        self.txtNICode = Entry(RightFrame2b, font=('arial', 12, 'bold'), bd=5, width=13, justify='left',
                               textvariable=NICode, state=DISABLED)
        self.txtNICode.grid(row=3, column=1)

        self.lblTaxablePay = Label(RightFrame2c, font=('arial', 12, 'bold'), text="\tTaxable Pay\t", bd=5)
        self.lblTaxablePay.grid(row=0, column=0, sticky=W)
        self.txtTaxablePay = Entry(RightFrame2c, font=('arial', 12, 'bold'), bd=5, width=13, justify='left',
                               textvariable=TaxablePay, state=DISABLED)
        self.txtTaxablePay.grid(row=0, column=1)

        self.lblPensionablePay = Label(RightFrame2c, font=('arial', 12, 'bold'), text="\tPensionable Pay\t", bd=5)
        self.lblPensionablePay.grid(row=1, column=0, sticky=W)
        self.txtPensionablePay = Entry(RightFrame2c, font=('arial', 12, 'bold'), bd=5, width=13, justify='left',
                                   textvariable=PensionablePay, state=DISABLED)
        self.txtPensionablePay.grid(row=1, column=1)

        self.lblNetPay = Label(RightFrame2d, font=('arial', 12, 'bold'), text="\tNet Pay\t", bd=5)
        self.lblNetPay.grid(row=0, column=0, sticky=W)
        self.txtNetPay = Entry(RightFrame2d, font=('arial', 12, 'bold'), bd=5, width=21, justify='left',
                                       textvariable=NetPay, state=DISABLED)
        self.txtNetPay.grid(row=0, column=1)

        #======================================================================================================================
        self.lblReference = Label(LeftFrame1, font=('arial', 12, 'bold'), text="\tReference\t", bd=10)
        self.lblReference.grid(row=0, column=0, sticky=W)
        self.txtReference = Entry(LeftFrame1, font=('arial', 12, 'bold'), bd=5, width=57, justify='left',
                               textvariable=Reference, state=DISABLED)
        self.txtReference.grid(row=0, column=1)

        self.lblEmployerName = Label(LeftFrame1, font=('arial', 12, 'bold'), text="\tEmployer Name\t", bd=10)
        self.lblEmployerName.grid(row=1, column=0, sticky=W)
        self.txtEmployerName = Entry(LeftFrame1, font=('arial', 12, 'bold'), bd=5, width=57, justify='left',
                                  textvariable=EmployerName)
        self.txtEmployerName.grid(row=1, column=1)

        self.lblEmployeeName = Label(LeftFrame1, font=('arial', 12, 'bold'), text="\tEmployee Name\t", bd=10)
        self.lblEmployeeName.grid(row=2, column=0, sticky=W)
        self.txtEmployeeName = Entry(LeftFrame1, font=('arial', 12, 'bold'), bd=5, width=57, justify='left',
                                     textvariable=EmployeeName, state=DISABLED)
        self.txtEmployeeName.grid(row=2, column=1)

        #======================================================================================================================
        self.lblCityWeighting = Label(LeftFrame2Left, font=('arial', 12, 'bold'), text="City Weighting", bd=10, anchor='e')
        self.lblCityWeighting.grid(row=0, column=0, sticky=W)
        self.txtCityWeighting = Entry(LeftFrame2Left, font=('arial', 12, 'bold'), bd=5, width=20, justify='left',
                                     textvariable=CityWeighting)
        self.txtCityWeighting.grid(row=0, column=1)

        self.lblBasicSalary = Label(LeftFrame2Left, font=('arial', 12, 'bold'), text="Basic Salary", bd=10)
        self.lblBasicSalary.grid(row=1, column=0, sticky=W)
        self.txtBasicSalary = Entry(LeftFrame2Left, font=('arial', 12, 'bold'), bd=5, width=20, justify='left',
                                      textvariable=BasicSalary)
        self.txtBasicSalary.grid(row=1, column=1)

        self.lblOverTime = Label(LeftFrame2Left, font=('arial', 12, 'bold'), text="Over Time", bd=10)
        self.lblOverTime.grid(row=2, column=0, sticky=W)
        self.txtOverTime = Entry(LeftFrame2Left, font=('arial', 12, 'bold'), bd=5, width=20, justify='left',
                                    textvariable=OverTime)
        self.txtOverTime.grid(row=2, column=1)

        self.lblOtherPaymentDue = Label(LeftFrame2Left, font=('arial', 12, 'bold'), text="Other Payment", bd=10)
        self.lblOtherPaymentDue.grid(row=3, column=0, sticky=W)
        self.txtOtherPaymentDue = Entry(LeftFrame2Left, font=('arial', 12, 'bold'), bd=5, width=20, justify='left',
                                 textvariable=OtherPaymentDue)
        self.txtOtherPaymentDue.grid(row=3, column=1)

        #======================================================================================================================
        self.lblTax = Label(LeftFrame2Right, font=('arial', 12, 'bold'), text="Tax", bd=10,
                                      anchor='e')
        self.lblTax.grid(row=0, column=0, sticky=W)
        self.txtTax = Entry(LeftFrame2Right, font=('arial', 12, 'bold'), bd=5, width=20, justify='left',
                                      textvariable=Tax, state=DISABLED)
        self.txtTax.grid(row=0, column=1)

        self.lblPension = Label(LeftFrame2Right, font=('arial', 12, 'bold'), text="Pension", bd=10)
        self.lblPension.grid(row=1, column=0, sticky=W)
        self.txtPension = Entry(LeftFrame2Right, font=('arial', 12, 'bold'), bd=5, width=20, justify='left',
                            textvariable=Pension, state=DISABLED)
        self.txtPension.grid(row=1, column=1)

        self.lblStudentLoan = Label(LeftFrame2Right, font=('arial', 12, 'bold'), text="Student Loan",bd=10)
        self.lblStudentLoan.grid(row=2, column=0, sticky=W)
        self.txtStudentLoan = Entry(LeftFrame2Right, font=('arial', 12, 'bold'), bd=5, width=20, justify='left',
                                textvariable=StudentLoan, state=DISABLED)
        self.txtStudentLoan.grid(row=2, column=1)

        self.lblNIPayment = Label(LeftFrame2Right, font=('arial', 12, 'bold'), text="NIPayment", bd=10)
        self.lblNIPayment.grid(row=3, column=0, sticky=W)
        self.txtNIPayment = Entry(LeftFrame2Right, font=('arial', 12, 'bold'), bd=5, width=20, justify='left',
                                    textvariable=NIPayment, state=DISABLED)
        self.txtNIPayment.grid(row=3, column=1)

        # ======================================================================================================================
        self.lblGrossPay = Label(LeftFrame3Left, font=('arial', 12, 'bold'), text="Gross Pay", bd=10)
        self.lblGrossPay.grid(row=3, column=0, sticky=W)
        self.txtGrossPay = Entry(LeftFrame3Left, font=('arial', 12, 'bold'), bd=5, width=30, justify='left',
                            textvariable=GrossPay, state=DISABLED)
        self.txtGrossPay.grid(row=3, column=1)

        self.lblDeductions = Label(LeftFrame3Right, font=('arial', 12, 'bold'), text="Deductions", bd=10)
        self.lblDeductions.grid(row=3, column=0, sticky=W)
        self.txtDeductions = Entry(LeftFrame3Right, font=('arial', 12, 'bold'), bd=5, width=28, justify='left',
                                 textvariable=Deductions, state=DISABLED)
        self.txtDeductions.grid(row=3, column=1)

        # ======================================Calculator========================================================
        self.txtDisplay = Entry(RightFrame1a, font=('arial', 19, 'bold'), bd=5, insertwidth=4, justify='right',
                                   textvariable=text_Input)
        self.txtDisplay.grid(row=0, column=0, columnspan=4)

        self.btnDigit7 = Button(RightFrame1a, padx=6, pady=6, bd=2,font=('arial', 16, 'bold'), width=4,
                                text="7", command=lambda:btnClick(7)).grid(row=1, column=0)
        self.btnDigit8 = Button(RightFrame1a, padx=6, pady=6, bd=2, font=('arial', 16, 'bold'), width=4,
                                text="8", command=lambda:btnClick(8)).grid(row=1, column=1)
        self.btnDigit9 = Button(RightFrame1a, padx=6, pady=6, bd=2, font=('arial', 16, 'bold'), width=4,
                                text="9", command=lambda:btnClick(9)).grid(row=1, column=2)
        self.btnAdd = Button(RightFrame1a, padx=6, pady=6, bd=2, font=('arial', 16, 'bold'), width=4,
                                text="+", command=lambda:btnClick("+")).grid(row=1, column=3)

        # ======================================================================================================================
        self.btnDigit4 = Button(RightFrame1a, padx=6, pady=6, bd=2, font=('arial', 16, 'bold'), width=4,
                                text="4", command=lambda:btnClick(4)).grid(row=2, column=0)
        self.btnDigit5 = Button(RightFrame1a, padx=6, pady=6, bd=2, font=('arial', 16, 'bold'), width=4,
                                text="5", command=lambda:btnClick(5)).grid(row=2, column=1)
        self.btnDigit6 = Button(RightFrame1a, padx=6, pady=6, bd=2, font=('arial', 16, 'bold'), width=4,
                                text="6", command=lambda:btnClick(6)).grid(row=2, column=2)
        self.btnSub = Button(RightFrame1a, padx=6, pady=6, bd=2, font=('arial', 16, 'bold'), width=4,
                             text="-", command=lambda:btnClick("-")).grid(row=2, column=3)

        # ======================================================================================================================
        self.btnDigit1 = Button(RightFrame1a, padx=6, pady=6, bd=2, font=('arial', 16, 'bold'), width=4,
                                text="1", command=lambda:btnClick(1)).grid(row=3, column=0)
        self.btnDigit2 = Button(RightFrame1a, padx=6, pady=6, bd=2, font=('arial', 16, 'bold'), width=4,
                                text="2", command=lambda:btnClick(2)).grid(row=3, column=1)
        self.btnDigit3 = Button(RightFrame1a, padx=6, pady=6, bd=2, font=('arial', 16, 'bold'), width=4,
                                text="3", command=lambda:btnClick(3)).grid(row=3, column=2)
        self.btnMul = Button(RightFrame1a, padx=6, pady=6, bd=2, font=('arial', 16, 'bold'), width=4,
                             text="*", command=lambda:btnClick("*")).grid(row=3, column=3)

        # ======================================================================================================================
        self.btnDigit0 = Button(RightFrame1a, padx=6, pady=6, bd=2, font=('arial', 16, 'bold'), width=4,
                                text="0", command=lambda:btnClick(0)).grid(row=4, column=0)
        self.btnClear = Button(RightFrame1a, padx=6, pady=6, bd=2, font=('arial', 16, 'bold'), width=4,
                                text="C", command=btnClear).grid(row=4, column=1)
        self.btnEqual = Button(RightFrame1a, padx=6, pady=6, bd=2, font=('arial', 16, 'bold'), width=4,
                                text="=", command=btnEquals).grid(row=4, column=2)
        self.btnDiv = Button(RightFrame1a, padx=6, pady=6, bd=2, font=('arial', 16, 'bold'), width=4,
                             text="/", command=lambda:btnClick("/")).grid(row=4, column=3)

        # ======================================================================================================================
        self.btnWages = Button(RightFrame1b, padx=16, pady=0, bd=5, font=('arial', 14, 'bold'), width=4,
                               text="Wages", command=Payment_Function).grid(row=0, column=0)
        self.btnDisplay = Button(RightFrame1b, padx=16, pady=0, bd=5, font=('arial', 14, 'bold'), width=4,
                               text="Display", command=addData).grid(row=0, column=1)
        self.btnUpdate = Button(RightFrame1b, padx=16, pady=0, bd=5, font=('arial', 14, 'bold'), width=4,
                             text="Update", command=update).grid(row=0, column=2)
        self.btnDelete = Button(RightFrame1b, padx=16, pady=0, bd=5, font=('arial', 14, 'bold'), width=4,
                               text="Delete", command=deleteDB).grid(row=1, column=0)
        self.btnReset = Button(RightFrame1b, padx=16, pady=0, bd=5, font=('arial', 14, 'bold'), width=4,
                                 text="Reset", command=Reset).grid(row=1, column=1)
        self.btnExit = Button(RightFrame1b, padx=16, pady=0, bd=5, font=('arial', 14, 'bold'), width=4,
                                text="Exit", command=iExit).grid(row=1, column=2)

        # ======================================================================================================================
        TopFrame11 = Frame(Tab2Frame, bd=10, width=1340, height=100,relief=RIDGE)
        TopFrame11.grid(row=0, column=0)
        TopFrame12 = Frame(Tab2Frame, bd=10, width=1340, height=100, relief=RIDGE)
        TopFrame12.grid(row=1, column=0)
        # ======================================================================================================================
        self.lblTitle = Label(TopFrame11, bd=10, font=('arial', 40, 'bold'), text="\tPayroll Management System\t",
                              justify=CENTER)
        self.lblTitle.grid(padx=72)
        # ======================================================================================================================
        scroll_x = Scrollbar(TopFrame12, orient=HORIZONTAL)
        scroll_y = Scrollbar(TopFrame12, orient=VERTICAL)

        self.payroll_records = ttk.Treeview(TopFrame12, height=22, columns=("ref", "fullname", "address", "cityweighting"
                                                                            , "basicsalary", "overtime", "grosspay", "tax"
                                                                            , "pension", "nipayment", "deductions",
                                                                            "postcode", "gender", "payday", "taxperiod",
                                                                             "taxcode", "ninumber", "netpay"),
                                            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.payroll_records.heading("ref", text="Reference")
        self.payroll_records.heading("fullname", text="Name")
        self.payroll_records.heading("address", text="Address")
        self.payroll_records.heading("cityweighting", text="City Weighting")

        self.payroll_records.heading("basicsalary", text="Basic Salary")
        self.payroll_records.heading("overtime", text="Over Time")
        self.payroll_records.heading("grosspay", text="Gross Pay")
        self.payroll_records.heading("tax", text="Tax")

        self.payroll_records.heading("pension", text="Pension")
        self.payroll_records.heading("nipayment", text="NI Payment")
        self.payroll_records.heading("deductions", text="Deductions")
        self.payroll_records.heading("postcode", text="Postcode")
        self.payroll_records.heading("gender", text="Gender")

        self.payroll_records.heading("payday", text="Payday")
        self.payroll_records.heading("taxperiod", text="Tax Period")
        self.payroll_records.heading("taxcode", text="Tax Code")
        self.payroll_records.heading("ninumber", text="NI Number")
        self.payroll_records.heading("netpay", text="Netpay")

        self.payroll_records['show'] = 'headings'

        self.payroll_records.column("ref", width=70)
        self.payroll_records.column("fullname", width=150)
        self.payroll_records.column("address", width=150)
        self.payroll_records.column("cityweighting", width=70)

        self.payroll_records.column("basicsalary", width=70)
        self.payroll_records.column("overtime", width=70)
        self.payroll_records.column("grosspay", width=70)
        self.payroll_records.column("tax", width=70)

        self.payroll_records.column("pension", width=70)
        self.payroll_records.column("nipayment", width=70)
        self.payroll_records.column("deductions", width=70)
        self.payroll_records.column("postcode", width=70)
        self.payroll_records.column("gender", width=70)

        self.payroll_records.column("payday", width=70)
        self.payroll_records.column("taxperiod", width=70)
        self.payroll_records.column("taxcode", width=70)
        self.payroll_records.column("ninumber", width=70)
        self.payroll_records.column("netpay", width=70)

        self.payroll_records.pack(fill=BOTH, expand=1)
        self.payroll_records.bind("<ButtonRelease-1>", WagesInfo)
        DisplayData()

        # ======================================================================================================================
        TopFrame13 = Frame(Tab3Frame, bd=10, width=1340, height=100, relief=RIDGE)
        TopFrame13.grid(row=0, column=0)
        # ======================================================================================================================
        self.lblNote = Label(TopFrame13, bd=10, font=('arial', 40, 'bold'), text="\tPayroll Note Book\t", justify=CENTER)
        self.lblNote.grid(row=0, column=0)

        # ======================================================================================================================
        self.txtNote = Text(TopFrame13, width=120, height=22, font=('arial', 14, 'bold'))
        self.txtNote.grid(row=1, column=0)
        # ======================================================================================================================


if __name__ == '__main__':
    root = Tk()
    application = Payroll(root)
    root.mainloop()

