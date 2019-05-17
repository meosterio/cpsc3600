Alex Moore
CPSC 3600
RDT 3.0 Implementation


I implemented the RDT 3.0 Transport layer, transitioning from A -> B -> A.
The transport is one way traffic, meaning only A is sending valuable
payload over to B. B really only sends back an ACK to A telling A that it
received the correct packet.

In the GBN, there is a known problem that depending on the time in which
packets are sent back to A from B, there might be an error regarding
index out of bounds. I started GBN and have a foundation that is working,
but I do not believe it is complete. If it is complete than woohoo!
