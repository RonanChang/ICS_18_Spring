S_ALONE = 0
S_TALKING = 1

#==============================================================================
# Group class:
# member fields: 
#   - An array of items, each a Member class
#   - A dictionary that keeps who is a chat group
# member functions:
#    - join: first time in
#    - leave: leave the system, and the group
#    - list_my_peers: who is in chatting with me?
#    - list_all: who is in the system, and the chat groups
#    - connect: connect to a peer in a chat group, and become part of the group
#    - disconnect: leave the chat group but stay in the system
#==============================================================================

class Group:
    
    def __init__(self):
        self.members = {}
        self.chat_grps = {}
        self.grp_ever = 0
        
    def join(self, name):
        self.members[name] = S_ALONE
        return
        
        
    #implement        
    def is_member(self, name):
        return name in self.memebers.keys()

            
    #implement
    def leave(self, name):
        self.disconnect(name)
        del self.members[name]
        return
        
    #implement                
    def find_group(self, name):        
        found = False
        group_key = 0
        for k in self.chat_grps.keys():
            if name in self.chat_grps[k]:
                found = True
                group_key = k
                break
        return found, group_key
        
    #implement                
    def connect(self, me, peer):
        #if peer is in a group, join it
        peer_in_group, group_key = self.find_group(peer)
        # otherwise, create a new group with you and your peer
        if peer_in_group:
            print(peer," is already in a group. Join the chat!")
            self.chat_grps[group_key].append(me)
            self.members[me] = S_TALKING
        else:
            print(peer, " is also alone!")
            self.grp_ever += 1
            self.chat_grps[self.grp_ever] = [me,peer]
            self.members[me] = S_TALKING
            self.members[peer] = S_TALKING
        print(self.list_me(me))
        return

    #implement                
    def disconnect(self, me):
        # find myself in the group, quit
        isInGroup,group_key = self.find_group(me)
        if isInGroup:
            self.chat_grps[group_key].remove(me)
            self.members[me] = S_ALONE
            if len(self.chat_grps[group_key]) == 1:
                peer = self.chat_grps[group_key].pop()
                self.members[peer] = S_ALONE
                del self.chat_grps[group_key]
        return
        
    def list_all(self):
        # a simple minded implementation
        full_list = "Users: ------------" + "\n"
        full_list += str(self.members) + "\n"
        full_list += "Groups: -----------" + "\n"
        full_list += str(self.chat_grps) + "\n"
        return full_list

    #implement
    def list_me(self, me):
        # return a list, "me" followed by other peers in my group
        my_list = []
        isInGroup,group_key = self.find_group(me)
        if isInGroup:
            my_list.append(me)
            for m in self.chat_grps[group_key]:
                if m != me:
                    my_list.append(m)           
        return my_list

if __name__ == "__main__":
	g = Group()
	g.join('a')
	g.join('b')
	print(g.list_all())

	g.connect('a', 'b')
	print(g.list_all())
