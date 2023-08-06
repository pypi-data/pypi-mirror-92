# coding=utf-8
from .utils import ObjectDict


class ZeekRule:
    def __init__(self, rule):
        self.ruleinfo = rule

    def genersigtext(self):
        _sigrules = ObjectDict(
            rulename=f'signature {self.ruleinfo.get("rulename")} {{',
            srcip=f'    src-ip == {self.ruleinfo.get("srcip")}',
            dstip=f'    dst-ip == {self.ruleinfo.get("dstip")}',
            srcport=f'    src-port == {self.ruleinfo.get("srcport")}',
            dstport=f'    dst-port == {self.ruleinfo.get("dstport")}',
            ipproto=f'    ip-proto == {self.ruleinfo.get("ipproto")}',
            condition=f'    {self.ruleinfo.get("condition")}',
            tcpstate=f'    tcp-state {self.ruleinfo.get("tcpstate")} ',
            depend=f'    {self.ruleinfo.get("depend")} ',
            ruledes=f'    event "{self.ruleinfo.get("ruledes")}"\n}}'
        )

        return '\n'.join([getattr(_sigrules, _) for _ in _sigrules.keys() if (_ in self.ruleinfo.keys() and self.ruleinfo.get(_))])

    def generzeektext(self):
        identifire = ""
        zeekruletext = f"""@load base/frameworks/signatures/main
@load base/utils/addrs
@load base/utils/directions-and-hosts

@load-sigs ./{self.ruleinfo.get("rulename")}.sig
module {self.ruleinfo.get("rulename")};

redef LogAscii::use_json = T;
redef Signatures::ignored_ids += /^{self.ruleinfo.get("rulename")}/;
export {{redef enum Notice::Type += {{{self.ruleinfo.get("rulename")}}};}}

event signature_match(state: signature_state, msg: string, data: string)
    {{
        if ( /{self.ruleinfo.get("rulename")}/ !in state$sig_id ) return;
        NOTICE([$note={self.ruleinfo.get("rulename")},
            $conn=state$conn,
            $msg=msg,
            $sub=data,
            $n=%s,
            $identifier=cat(%s),
            $suppress_for=%smin
            ]);
    }}
        """
        for _ in self.ruleinfo.get("identifier").split(','):
            identifire += "state$conn$id$" + _ + ','
        zeekruletext = zeekruletext % (self.ruleinfo.get(   "notice"), identifire.strip(','),
                                       self.ruleinfo.get("suppress_for"))
        return zeekruletext

    def generrule(self):
        return {"rulename": self.ruleinfo.get("rulename"), "zeekruletext": self.generzeektext(),
                "sigruletext": self.genersigtext()}