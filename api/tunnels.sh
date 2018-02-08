ssh -L 9042:192.168.1.97:9042 pstehlik@130.186.16.82 -N &
cassandra=$!
ssh -L 8000:192.168.1.97:8083 pstehlik@130.186.16.82 -N &
kairos=$!

echo "Kairos:$kairos"
echo "Cassandra: $cassandra"
