theory ModusPonens
  imports Main
begin

lemma modus_ponens: "P \<longrightarrow> Q \<Longrightarrow> P \<Longrightarrow> Q"
proof -
  assume a1: "P \<longrightarrow> Q"
  assume a2: "P"
  from a1 a2 show "Q" by (rule mp)
qed

end
