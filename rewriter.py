from NajaListener import NajaListener
from semanticException import SemanticException

from queue import Queue
import os

class RewriteListener(NajaListener):

  #Chave dos Dicionarios = Nome das Variaveis
  dicTipos = {}
  dicUtilizacao = {}
  q = Queue()
  tab = 0
  
  def addVariavel(self, nomeVariavel, tipoVariavel):
    self.dicTipos[nomeVariavel] = tipoVariavel
    self.dicUtilizacao[nomeVariavel] = False

  def verificaVariavelDeclarada(self, nomeVariavel):
    if self.dicTipos.get(nomeVariavel) == None:
      raise SemanticException(f"Variable not declared: {nomeVariavel}.")

  def verificaCompatibilidadeTipo(self, var1, var2):
    if self.dicTipos.get(var1) != self.dicTipos.get(var2):
      raise SemanticException(f"Type Mismatch between Variables {var1} and {var2}.")

  # Exit a parse tree produced by ArrayInitParser#init.
  def exitDeclaravar(self, ctx):
      type = ctx.tipo().getText()
      vars = ctx.ID()

      for var in vars:
        variable = var.getText()
        if type == 'texto':
          self.q.put("  "*self.tab + variable + " = " + '\'\'')
        else: self.q.put("  "*self.tab + variable + " = " + "0")
        self.addVariavel(variable, type)

  def exitCmdleitura(self, ctx):
    id = ctx.ID().getText()
    self.verificaVariavelDeclarada(id)
    self.dicUtilizacao[id] = True
    if self.dicTipos.get(id) == 'numero':
      self.q.put("  "*self.tab + id + " = float(input())")
    else:
      self.q.put("  "*self.tab + id + " = input()")
  
  def exitCmdescrita(self, ctx):
    id = ctx.escrita().getText()
    if id[0] != "\"" or id[len(id) - 1] != "\"":
      self.verificaVariavelDeclarada(id)
      self.dicUtilizacao[id] = True
    
    self.q.put("  "*self.tab +"print(" + id + ")")

  def exitCmdattrib(self, ctx):
    self.verificaVariavelDeclarada(ctx.ID().getText())
    self.dicUtilizacao[ctx.ID().getText()] = True
    
    tipoID = self.dicTipos.get(ctx.ID().getText())
    Expr = ctx.expr().getText()

    if "\"" in Expr:
      tipoExpr = 'texto'
    else: tipoExpr = 'numero'

    if tipoID != tipoExpr: 
      raise SemanticException(f"Type Mismatch - Variable of Type {tipoID} receiving Type {tipoExpr}.")

    exprs = ctx.expr().getText().replace('.', '*')
    self.q.put("  "*self.tab + ctx.ID().getText() + " = " + str(exprs))

  def enterCmdselecao(self, ctx):
    self.q.put("  "*self.tab + "if " + ctx.cmdcondicao().getText() + ":")
    self.tab += 1

  def exitCmdselecao(self, ctx):
    self.tab -= 1
  
  def enterCmdelse(self, ctx):
    self.q.put("  "*(self.tab - 1) + "else:")
  
  def enterCmdenquanto(self, ctx):
    self.q.put("  "*self.tab + "while " + ctx.cmdcondicao().getText() + ":")
    self.tab += 1

  def exitCmdenquanto(self, ctx):
    self.tab -= 1

  def enterCmdexecute(self, ctx):
    self.q.put("  "*self.tab + "while True:")
    self.tab += 1

  def exitCmdexecute(self, ctx):
    self.q.put("  "*self.tab + "if not" + ctx.cmdcondicao().getText() + ":")
    self.q.put("  "*(self.tab + 1) + "break")
    self.tab -= 1

  def exitCmdcondicao(self, ctx):
    vars = ctx.ID()
    numbers = ctx.NUMBER()
    
    for var in vars:
      self.verificaVariavelDeclarada(var.getText())
      self.dicUtilizacao[var.getText()] = True
      if numbers != None and self.dicTipos.get(var.getText()) == 'texto':
        raise SemanticException(f"Type Mismatch - It can not operate a String with a Number.") 

  def exitExpr(self, ctx):
    IDs = ctx.termo()

    for id in IDs:
      if self.dicTipos.get(id.getText()) != None:
        if self.dicTipos.get(id.getText()) != 'numero':
          raise SemanticException(f"Type Mismatch - It can not operate a String with a Number.")
    
  def exitTermo(self, ctx):
    id = ctx.ID()
    
    if id != None:
      self.verificaVariavelDeclarada(id.getText())
      self.dicUtilizacao[id.getText()] = True

  def exitProg(self, ctx):
    lNaoUsadas = []

    for key, value in self.dicUtilizacao.items():
      if value == False:
        lNaoUsadas.append(key)

    if lNaoUsadas != []:
      raise SemanticException(f"Unsed declared variables: {', '.join(lNaoUsadas)}")

    f = open("exit.py", "w")
    f.close()
    f = open("exit.py", "a")

    while (self.q.empty() == False):
      line = self.q.get()
      
      line = line.replace(',','.')

      f.write(line + "\n")

    f.close()