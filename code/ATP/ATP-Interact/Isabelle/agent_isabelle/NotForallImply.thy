theory NotForallImply
  imports Main
begin

(* 对应 Coq 中的 not_imply_iff 定理 *)
theorem not_imply_iff: 
  assumes "\<not> (P \<longrightarrow> Q)"
  shows "P \<and> \<not> Q"
  using assms by auto

(* 对应 Coq 中的 forall_iff 定理 *)
theorem forall_iff: 
  assumes "\<forall>x. (P x \<longleftrightarrow> Q x)"
  shows "(\<forall>x. P x) \<longleftrightarrow> (\<forall>x. Q x)"
  using assms by blast

(* 对应 Coq 中的 not_exists 定理 *)
theorem not_exists: 
  assumes "\<not> (\<exists>x. P x)"
  shows "\<forall>x. \<not> P x"
  using assms by auto

(* 对应 Coq 中的 not_forall 定理 *)
theorem not_forall: 
  assumes "\<not> (\<forall>x. P x)"
  shows "\<exists>x. \<not> P x"
  using assms by auto

(* 对应 Coq 中的 corollary not_forall_imply *)
corollary not_forall_imply: 
  assumes "\<not> (\<forall>x. P x \<longrightarrow> Q x)"
  shows "\<exists>x. P x \<and> \<not> Q x"
proof -
  obtain x where "\<not> (P x \<longrightarrow> Q x)"
    using not_forall[of "\<lambda>x. P x \<longrightarrow> Q x"] assms by auto
  hence "P x \<and> \<not> Q x"
    using not_imply_iff by auto
  thus ?thesis by blast
qed

end
