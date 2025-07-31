import pandas as pd
import random

from .root_account import Account
#what is that
print('sucessful imports')
# WHAT  IS JOURNALING???
# Journaling is tha first step in the accounting cycle
# To perform a transaction (and report it in the General Journal i.e. `Journaling.general_journal`)-
# the user or essentially accountants provide the date of the transactions- 
# , the acccounts affected by the transactions ,and the amount that the accounts are affected by
# In the case of this program it also provides random five digit IDs for each transaction-->(henceforth interchangably: entry, journal entry, record)

# READ THIS!!
# In a normal accounting cycle; at the end of each period accountants log-
# transactions made on each account in it's ledger and consolidates all of this in a 'General Ledger
# As far as this program is concerned:
    # 1. A general ledger is useless
    # 2. Logging transactions in ledgers is made automatically with each transaction
    # as opposed to being made at the end of the period
    # this reduces the amount of work that has to be made by the user
    # the user only needs to:
        # a. Create accounts
        # b. Initiate an instance of Journaling (could be automated later on in future releases)
        # c. Record transactions with the wanted accounts
        # d. Demand any statement they want.

# WHY THE PROGRAM SEEMS ADMITTEDLY A LITTLE BIT STUPID AND CLUMSY -->
# Practically a journal entry involves at least two aand at most three accounts
# The journal entry consists of two equal sides called debit (henceforth--> dr) and credit (henceforth--> cr)
# whether the transaction involves two or three accounts (henceforth di, tri for simplicity)-
# Debit should always equal credit
# WHAT MAKES this program a little bit clumsy is that it has to account for both transactions that are di and tri,
# di and tri have completley different dynamics, di entries are easy, 
# but tri entries require having two account debited and one credited or one debited or two credited
# this -unless there is a way to make this more abstract- doubles the amount of code needed
# so expect to find every functionality split to account for di and tri and sometimes di, tri01 and tri02

class Journaling:
    
    # This is the class attribute where all transactions are written
    general_journal = pd.DataFrame(columns=['id', 'date', 'account_name', 'pr', 'dr', 'cr'])
    used_accs = []
    entries = []

    def __init__(self):
        '''
        this way whenever we need all transactions made we find them in this list
        O(1)
        '''
        Journaling.entries.append(self)
    
    @classmethod
    def get_accounts(cls):
        '''
        to access the list of classes
        '''
        return cls.used_accs

    @classmethod
    def get_entries(cls):
        '''
        to access the list of entries
        '''
        return cls.entries
    
    def object_handling_di(self, dr_acc, cr_acc):
        '''
        Just makes sure the user doesn't enter a frappichino instead of an account
        O(mn) time complexity
        '''
        accounts = (dr_acc, cr_acc)
        for acc in accounts: #O(mn)
            
            if issubclass(Account, acc): 
                
                if acc not in self.used_accs: #O(n)
                    '''
                    If this is the first time the account is used this block runs and adds the to the list of used accounts
                    ''' 
                    self.used_accs.append(acc) #O(1)

            else:
                print(f'''{acc} may not be a properly defined account or isn\'t an account at all,
                      \nmake sure u entered an instance of `Root.Account`''')

    def object_handling_tri(self, dracc, acc02, cracc):        
        
        accounts = [dracc, acc02, cracc]
        for acc in accounts: #O(mn)
            
            if issubclass(Account, acc): 
                if acc not in self.used_accs: #O(n)
                     
                    self.used_accs.append(acc) #O(1)

            else:
                print(f'''{acc} may not be a properly defined account or isn\'t an account at all,
                      \nmake sure u entered an instance of `Root.Account`''')

    def log_entry_di(self, date, dr_acc, cr_acc, amount):
        '''
        logs the entry to the ledger of each account 
        O(mn)
        '''
        dr_acc.transaction(date, amount)
        cr_acc.transaction(date, 0 ,amount)

    def log_entry_tri(self, entry_type, date,
                  dracc, dracc_amount, 
                  acc02, acc02_amount, cracc):
        
        def two_dr(date, dracc, acc02, cracc, dracc_amount, acc02_amount):
            '''
            logs the entry to the ledger of each account
            this is a two dr & one cr 
            '''
            cracc_amount = dracc_amount + acc02_amount
            dracc.transaction(date, dracc_amount)
            acc02.transaction(date, acc02_amount)
            cracc.transaction(date, 0, cracc_amount)

        def two_cr(date, dracc, acc02, cracc, dracc_amount, acc02_amount):
            '''
            logs the entry to the ledger of each account 
            this is a one dr & two cr
            '''
            cracc_amount = dracc_amount - acc02_amount
            dracc.transaction(date, dracc_amount)
            acc02.transaction(date, 0, acc02_amount)
            cracc.transaction(date, 0, cracc_amount)

        if 'two_dr'== entry_type:
            '''
            `entry_type` will be decided inside `journalizing_...` later on
            '''
            two_dr(date, dracc, acc02, cracc, dracc_amount, acc02_amount)
        else:
            two_cr(date, dracc, acc02, cracc, dracc_amount, acc02_amount)

    def journalize_di(self, date:str, dr_acc:Account, cr_acc:Account, amount:float):
        '''
        Summons needed functions to chec validity and log transactions
        Then writes the entry
        O (mn)
        '''
        self.object_handling_di(dr_acc, cr_acc) #O(mn)
        self.log_entry_di(self, dr_acc, cr_acc, amount) #O(mn)
        
        rand_id = round(100000*(random.random()))
        
        dr_entry = pd.DataFrame([[rand_id, date, dr_acc.name, dr_acc.pr, amount, 0]]
                        , columns=['id', 'date', 'account_name', 'pr', 'dr', 'cr'])
        cr_entry = pd.DataFrame([[rand_id ,date, cr_acc.name, cr_acc.pr, 0, amount]]
                        , columns=['id', 'date', 'account_name', 'pr', 'dr', 'cr'])
        
        entry = pd.concat([dr_entry, cr_entry], ignore_index=True)

        self.general_journal = pd.concat([self.general_journal, entry], ignore_index=True)


    def journalize_tri(self, date:str, tri_type:str, 
                            dracc:Account, dracc_amount:float, 
                            acc02:Account, acc02_amount:float, 
                            cracc:Account):
        
        def two_dr(date, dracc, dracc_amount, acc02, acc02_amount, cracc):
                '''
                Summons needed functions to chec validity and log transactions
                Then writes the entry
                O (mn)
                '''
                cracc_amount = dracc_amount + acc02_amount # for the entry to be balance this shoould be true
                entry_type = 'two_dr' # variable that determaines which type of tri entry to use
                self.object_handling_tri(dracc, acc02, cracc)
                self.log_entry_tri(date, entry_type, dracc, acc02, cracc, dracc_amount, acc02_amount)

                rand_id = round(100000*(random.random()))

                dr_entry01 = pd.DataFrame([[rand_id, date, dracc.name, dracc.pr, dracc_amount, 0]]
                            , columns=['id', 'date', 'account_name', 'pr', 'dr', 'cr'])
                
                dr_entry02 = pd.DataFrame([[rand_id, date, acc02.name, acc02.pr, acc02_amount, 0]]
                            , columns=['id', 'date', 'account_name', 'pr', 'dr', 'cr'])

                cr_entry03 = pd.DataFrame([[rand_id,date, cracc.name, cracc.pr, 0, cracc_amount]]
                            , columns=['id', 'date', 'account_name', 'pr', 'dr', 'cr'])
                
                entry = pd.concat([dr_entry01, dr_entry02, cr_entry03], ignore_index=True)

                self.general_journal = pd.concat([self.general_journal, entry], ignore_index=True)
        
        def two_cr(date, dracc, dracc_amount, acc02, acc02_amount, cracc):
                
                cracc_amount = dracc_amount + acc02_amount
                entry_type = 'two_cr'
                
                self.log_entry_tri(date, entry_type, dracc, acc02, cracc, dracc_amount, acc02_amount)

                rand_id = round(100000*(random.random()))

                dr_entry01 = pd.DataFrame([[rand_id, date, dracc.name, dracc.pr, dracc_amount, 0]]
                            , columns=['id', 'date', 'account_name', 'pr', 'dr', 'cr'])
                cr_entry01 = pd.DataFrame([[rand_id, date, acc02.name, acc02.pr, acc02_amount, 0]]
                            , columns=['id', 'date', 'account_name', 'pr', 'dr', 'cr'])
                cr_entry02 = pd.DataFrame([[rand_id,date, cracc.name, cracc.pr, 0, cracc_amount]]
                            , columns=['id', 'date', 'account_name', 'pr', 'dr', 'cr'])
                entry = pd.concat([dr_entry01, cr_entry01, cr_entry02], ignore_index=True)
                self.general_journal = pd.concat([self.general_journal, entry], ignore_index=True)
            
        if 'two_dr' == tri_type:
            two_dr(date, dracc, dracc_amount, acc02, acc02_amount, cracc)
        
        else:
            two_cr(date, dracc, dracc_amount, acc02, acc02_amount, cracc)

            
        
    
    def entry_di(self, date:str, dr_acc:Account, cr_acc:Account, amount:float):
        '''
        Two accounts are entered; the first is always the debited account (this is a GAAP convention)
        We append both to a tuple and intiate a for-loop
        '''
        self.journalize_di(date, dr_acc, cr_acc, amount)

    def entry_tri(
            self, date:str, 
            dracc:Account, dracc_blnc, dracc_amount:float,
            acc02:Account, acc02_blnc, acc02_amount:float,
            cracc:Account
            ):
        '''
        Two accounts are entered; the first is always the debited account 
        and the third is always a credited account (its how double entry accounting works)
        the second is the problematic part of the program, it can be both
        so, `dracc_blnc` and `acc02_blnc` are used to decide, if they are both equal (the user could enter any value as long as the are equal)
        then `acc02` is debited, else, it is credited
        O(mn)
        '''
        if dracc_blnc == acc02_blnc:
            tri_type = 'two_dr'
            self.journalize_tri(date, tri_type, dracc, dracc_amount, acc02, acc02_amount, cracc)
        
        else:
            tri_type = 'two_cr'
            self.journalize_tri(date, tri_type, dracc, dracc_amount, acc02, acc02_amount, cracc)
    
    def all_accounts(self):
        return self.used_accs

print('i now know journaling')
