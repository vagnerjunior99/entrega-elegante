# --- ÁREA DO ADMINISTRADOR (PROTEGIDA POR SENHA) ---
st.markdown("---")
st.markdown("### 🛠️ Área do Administrador")

with st.expander("Clique aqui para acessar o painel de controle"):
    # Campo para digitação da senha
    senha_adm = st.text_input("Digite a senha master para liberar o relatório:", type="password")
    
    # Define a sua senha secreta aqui
    if senha_adm == "99food2026":
        st.success("Acesso autorizado! 🕵️‍♂️")
        
        if len(st.session_state.mensagens) > 0:
            df = pd.DataFrame(st.session_state.mensagens)
            
            df['Acertou?'] = df.apply(
                lambda r: "Sim" if r['palpite'].lower() in r['remetente'].lower() and r['palpite'] != "" else ("Não" if r['palpite_feito'] else "Não palpitou ainda"), 
                axis=1
            )
            
            df_relatorio = df[["data", "destinatario", "mensagem", "remetente", "palpite", "Acertou?"]]
            df_relatorio.columns = ["Data/Hora", "Quem Recebeu", "Mensagem", "Remetente Real (Anônimo)", "Palpite da Pessoa", "Acertou o Palpite?"]
            
            # Mostra uma prévia dos dados na tela apenas para o ADM
            st.dataframe(df_relatorio)
            
            csv = df_relatorio.to_csv(index=False).encode('utf-8-sig')
            
            st.download_button(
                label="📥 Baixar Planilha de Acertos (Excel/CSV)",
                data=csv,
                file_name="relatorio_final_entrega_elegante.csv",
                mime="text/csv"
            )
        else:
            st.text("Nenhum dado para exportar ainda.")
    elif senha_adm != "":
        st.error("Senha incorreta. Acesso negado!")
