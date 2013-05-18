from stream_writer import StreamWriter

s = StreamWriter('http://stream1.opb.org/kmhd.mp3', seconds=25.0)

s.record()
print s.stream_length
