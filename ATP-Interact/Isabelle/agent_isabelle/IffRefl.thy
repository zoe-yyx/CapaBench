theory IffRefl
  imports Main
begin

theorem iff_refl: "P \<longleftrightarrow> P"
proof (rule iffI)
  show "P \<Longrightarrow> P" by assumption
  show "P \<Longrightarrow> P" by assumption
qed

end
